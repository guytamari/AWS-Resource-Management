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





@app.route("/create-ec2", methods=["POST"])
def create_ec2():
    instance_type = request.form.get("instance_type")
    print(instance_type)
    ami_choice = request.form.get("ami")
    tag_name = request.form.get("tag_name")
    num_instances = request.form.get("num_instances", "1")
    os.environ["INSTANCE_TYPE"] = instance_type
    os.environ["AMI"] = ami_choice
    os.environ["TAG_NAME"] = tag_name
    os.environ["NUM_INSTANCES"] = num_instances
    subprocess.run(["pulumi", "refresh", "--yes"], cwd="pulumi_project")
    subprocess.run(["pulumi", "up", "--yes"], cwd="pulumi_project")
    return redirect(url_for("home"))


@app.route("/ec2/instances", methods=["GET"])
def get_ec2_instances():
    try:
        with open("./pulumi_project/ec2_instances.json", "r") as f:
            instances_data = json.load(f)
        return jsonify({"instances": instances_data})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/ec2/start', methods=['POST'])
def start_instance():
    instance_id = request.json.get("instance_id")
    response = ec2_client.start_instances(InstanceIds=[instance_id])
    return jsonify({"status": "Starting", "instance_id": instance_id})

@app.route('/ec2/stop', methods=['POST'])
def stop_instance():
    instance_id = request.json.get("instance_id")
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    return jsonify({"status": "Stopping", "instance_id": instance_id})

@app.route('/ec2/restart', methods=['POST'])
def restart_instance():
    instance_id = request.json.get("instance_id")
    response = ec2_client.reboot_instances(InstanceIds=[instance_id])
    return jsonify({"status": "Restarting", "instance_id": instance_id})

if __name__ == "__main__":
    app.run(debug=True)
