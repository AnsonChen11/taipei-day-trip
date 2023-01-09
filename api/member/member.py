from flask import Blueprint, render_template, request, jsonify
from modules import connect_to_db
from modules.connect_to_db import conn
from .models import *
import os, boto3, base64
from dotenv import load_dotenv

member = Blueprint(
    'member', __name__,
    static_folder='static',
    template_folder='templates'
    )

@member.route("/member")
def base():
    data = get_auth_data()
    if data == False:
        return render_template("index.html")

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

    response = s3.get_object(
    Bucket = "taipeitripbucket",
    Key = file.filename,
    )

    image_data = response["Body"].read()
    image_url = base64.b64encode(image_data).decode("utf-8")
    return jsonify({
        "image_url": image_url
        }), 200 


# @member.route("/api/get-image-url", methods=["GET"])
# def get_image_url():
#   # 调用S3 REST API的GET Object操作获取图片的URL
#   image_url = ...

#   return jsonify({"image_url": image_url}), 200   