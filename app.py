from flask import Flask, render_template,request, redirect, url_for, jsonify
import json
import subprocess
import os
import boto3
ec2_client = boto3.client('ec2')
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

@app.route('/create-s3', methods=["POST"])
def create_s3():
    bucket_name = request.form.get("bucket_name")
    access_type = request.form.get("access_type")
    os.environ["BUCKET_NAME"] = bucket_name
    os.environ["ACCESS_TYPE"] = access_type
    files = request.files.getlist('file_upload')
    
    if files:
        for file in files:
            # save the file in temps
            file.save(os.path.join("temp", file.filename))
    env = os.environ.copy()  
    env["PULUMI_STACK"] = "s3"
    from pulumi_project.scripts.create_s3 import s3
    print(s3)
    # # subprocess.run(["pulumi", "refresh","--stack","s3", "--yes"], cwd="pulumi_project",env=env)
    # subprocess.run(["pulumi", "up","--stack","s3", "--yes"], cwd="pulumi_project",env=env)
    return redirect(url_for("home"))




if __name__ == "__main__":
    app.run(debug=True)
