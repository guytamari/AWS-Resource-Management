from flask import Flask, render_template,request, redirect, url_for, jsonify
import json
import subprocess
import os
import boto3
ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ec2")
def ec2():
    return render_template("ec2.html")

@app.route("/ec2/spec-ec2")
def spec_ec2():
    return render_template("spec-ec2.html")

@app.route("/route53")
def route53():
    return render_template("route53.html")

@app.route("/s3")
def s3():
    return render_template("s3.html")


@app.route("/s3/spec-s3")
def spec_s3():
    return render_template("spec-s3.html")




# ---------------------------------------------------------------
# ec2 management and creations
@app.route("/create-ec2", methods=["POST"])
def create_ec2():
    instance_type = request.form.get("instance_type")
    ami_choice = request.form.get("ami")
    tag_name = request.form.get("tag_name")
    num_instances = request.form.get("num_instances", "1")
    os.environ["INSTANCE_TYPE"] = instance_type
    os.environ["AMI"] = ami_choice
    os.environ["TAG_NAME"] = tag_name
    os.environ["NUM_INSTANCES"] = num_instances
    env = os.environ.copy()
    env["PULUMI_STACK"] = "dev"
    subprocess.run(["pulumi", "refresh", "--stack","dev","--yes"], cwd="pulumi_project",env=env)
    subprocess.run(["pulumi", "up", "--stack","dev", "--yes"], cwd="pulumi_project",env=env)
    return redirect(url_for("home"))


@app.route("/ec2/instances", methods=["GET"])
def get_ec2_instances():
    try:
        with open("./pulumi_project/ec2_instances.json", "r") as f:
            instances_data = json.load(f)
        return jsonify({"instances": instances_data})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
def change_instance_state(action):
    instance_id = request.json.get("instance_id")
    
    if action == 'start':
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        status = "Starting"
    elif action == 'stop':
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        status = "Stopping"
    elif action == 'restart':
        response = ec2_client.reboot_instances(InstanceIds=[instance_id])
        status = "Restarting"
    
    return jsonify({"status": status, "instance_id": instance_id})

@app.route('/ec2/start', methods=['POST'])
def start_instance():
    return change_instance_state('start')

@app.route('/ec2/stop', methods=['POST'])
def stop_instance():
    return change_instance_state('stop')

@app.route('/ec2/restart', methods=['POST'])
def restart_instance():
    return change_instance_state('restart')


# ec2 management and creations
# ---------------------------------------------------------------



# ---------------------------------------------------------------
# s3 management and creations



def calling_the_s3_creation(is_files, temp_files):
    if is_files:
        from pulumi_project.scripts.create_s3 import create_s3, upload_files_to_s3
        s3 = create_s3()
        upload_files_to_s3(temp_files)
        print(s3)
    else:
        from pulumi_project.scripts.create_s3 import create_s3
        s3 = create_s3()
        print(s3)

        
        


@app.route('/create-s3', methods=["POST"])
def create_s3():
    bucket_name = request.form.get("bucket_name")
    access_type = request.form.get("access_type")
    os.environ["BUCKET_NAME"] = bucket_name
    os.environ["ACCESS_TYPE"] = access_type
    files = request.files.getlist('file_upload')
    

    
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    if any(file.filename for file in files):
        temp_files = []
        for file in files:
            temp_path = os.path.join("temp", file.filename)
            file.save(temp_path)
            temp_files.append(temp_path)

        calling_the_s3_creation(True, temp_files)

        for temp_file in temp_files:
            os.remove(temp_file)
    else:
        calling_the_s3_creation(False, None)
    
    return redirect(url_for("home"))


@app.route('/s3/buckets', methods=["GET"])
def fetch_s3():
    from pulumi_project.scripts.fetch_s3 import fetch_s3_buckets
    return fetch_s3_buckets()



@app.route('/s3/delete', methods=["POST"])
def delete_bucket():
    data = request.json
    bucket_name = data.get("bucket_name")

    if not bucket_name:
        return jsonify({"error": "Bucket name is required"}), 400

    # delete all files inside the bucket
    objects = s3_client.list_objects_v2(Bucket=bucket_name)
    if "Contents" in objects:
        for obj in objects["Contents"]:
            s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])

    # delete the bucket itself
    s3_client.delete_bucket(Bucket=bucket_name)

    return jsonify({"status": "Bucket deleted successfully"}), 200



@app.route('/s3/upload', methods=["POST"])
def upload_file():
    bucket_name = request.form.get("bucket_name")
    file = request.files["file"]

    s3_client.upload_fileobj(file, bucket_name, file.filename)

    return jsonify({"status": "File uploaded successfully"}), 200



# s3 management and creations
# ---------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
