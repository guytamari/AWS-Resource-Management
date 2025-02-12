from flask import Flask, render_template

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





if __name__ == "__main__":
    app.run(debug=True)
