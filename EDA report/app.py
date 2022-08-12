from operator import contains
from flask import Flask,render_template,request,redirect
import pandas as pd
import pandas_profiling as pp
import smtplib
from email.message import EmailMessage 

app=Flask(__name__ ,template_folder ='template')
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")                      
def upload(): 
    return render_template("filetype.html")

@app.route("/file", methods=["POST","GET"])
def file():
    if request.method=="POST":
        f=request.files["file"]
        f.save(""+f.filename)    # If we need to mention the path where the file should be saved we can do 
        file_name=f.filename
        extension=file_name.split(".")[1]
        if extension=="csv":
            df=pd.read_csv(file_name)
        else:
            df=pd.read_excel(file_name)

        p=pp.ProfileReport(df)
        p.to_file(f"{file_name.split('.')[0]}_EDA.html")
        msg=EmailMessage()
        mail_sender=request.form["sender_mail"] 
        mail_id_password=request.form["mail_id_password"]
        msg["Subject"]=request.form["subject"] 
        msg["From"]=mail_sender
        msg["To"]=request.form["receiver_mail"] 
        msg.set_content("PFB I have attached your EDA report")
        file=f"{file_name.split('.')[0]}_EDA.html"
        with  open(file,"rb") as f:
            f_data=f.read()
            f_name=f.name
        msg.add_attachment(f_data,maintype="application",subtype="octet-stream",filename=f_name)

        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(mail_sender,mail_id_password)
            smtp.send_message(msg)   
        return "Mail Sent"
        #return render_template("table.html",tables=[df.to_html(classes='data')], titles=df.columns.values)


app.run(debug=True)