from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import json
import boto3

from src.shared.environments import Environments


envs = Environments.get_envs()

session = boto3.Session(
    aws_access_key_id=envs.aws_access_key_id,
    aws_secret_access_key=envs.aws_secret_access_key,
    region_name=envs.region
)

s3 = session.client('s3')
ses = session.client('ses')
def lambda_handler():
    try:
        obj = s3.get_object(Bucket=envs.s3_bucket_name, Key=envs.image_key)
        img = obj['Body'].read()

        email = MIMEMultipart()

        email["From"] = envs.sender_email
        email["To"] = envs.receiver_email
        email["Subject"] = "Desafio do Desenho Perdido de Charles!"

        mime = MIMEBase("image", "png")
        mime.set_payload(img)
        encoders.encode_base64(mime)
        mime.add_header("Content-Disposition", 'attachment' + '; ' + 'filename=' + f'"{envs.image_key}"')
        email.attach(mime)

        ses.send_raw_email(
            Source=envs.sender_email,
            Destinations=[envs.receiver_email],
            RawMessage={"Data": email.as_string()}
        )

        return {
            "statusCode": 200,
            "body": "E-mail enviado!"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Erro ao enviar e-mail. Erro: {str(e)}"
        }