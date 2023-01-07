from flask import Blueprint, render_template, request, jsonify
from modules import connect_to_db
from modules.connect_to_db import conn
import os, boto3
from dotenv import load_dotenv

member = Blueprint(
    'member', __name__,
    static_folder='static',
    template_folder='templates'
    )

@member.route("/member")
def base():
	return render_template("member.html")

@member.route("/upload", methods=['POST'])
def upload():
    load_dotenv()
    aws_access_key = os.getenv("aws_access_key")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
 
    s3 = boto3.client(
        "s3", 
        aws_access_key_id = aws_access_key,
        aws_secret_access_key = aws_secret_access_key,
        region_name = "ap-northeast-1"
    )

    file = request.files["file"]
    s3.upload_fileobj(file, "taipeitripbucket", file.filename)
    return jsonify("Success")