import datetime

import pymysql as pymysql
from flask import Flask, render_template, request, session, redirect

conn = pymysql.connect(host="localhost", user="root", password="maheshg@6714", db="SchoolManagementSystem")
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = "sfdgfdgdadf"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/aLogin")
def aLogin():
    return render_template("aLogin.html")


@app.route("/iLogin")
def iLogin():
    return render_template("iLogin.html")


@app.route("/sLogin")
def sLogin():
    return render_template("sLogin.html")


@app.route("/aLogin1",methods=['post'])
def aLogin1():
    Username = request.form.get("Username")
    password = request.form.get("password")
    if Username == 'admin' and password == 'admin':
        session['role'] = 'admin'
        return render_template("adminHome.html")
    else:
        return render_template("message.html", msg='Invalid Login Details', color='text-danger')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/adminHome")
def adminHome():
    return render_template("adminHome.html")

@app.route("/addDepartment")
def addDepartment():
    department_name = request.args.get("department_name")
    if department_name != None:
        result = cursor.execute("select * from department where department_name = '" + str(department_name) + "'")
        if result > 0:
            return render_template('message.html', msg='This Department "'+department_name+'" Already Exits', color='text-danger')
        else:
            cursor.execute("insert into department(department_name) values('" + str(department_name) + "') ")
            conn.commit()
    cursor.execute("select * from department")
    departments = cursor.fetchall()
    return render_template("addDepartment.html",department_name=department_name,departments=departments)


@app.route("/addInstructor")
def addInstructor():
    cursor.execute("select * from department")
    departments = cursor.fetchall()
    return render_template("addInstructor.html",departments=departments)


@app.route("/addInstructor1",methods=['post'])
def addInstructor1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    experience = request.form.get("experience")
    department_id = request.form.get("department_id")
    try:
        cursor.execute("insert into instructor(name,email,phone,password,experience,department_id) values('"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(experience)+"','"+str(department_id)+"')")
        conn.commit()
        return render_template("message.html", msg='Instructor Added Successfully', color='alert-success')
    except Exception as e:
        print(e)
        return render_template("message.html",msg='Something Went Wrong',color='alert-danger')

@app.route("/viewInstructors")
def viewInstructors():
    cursor.execute("select * from instructor")
    instructors = cursor.fetchall()
    return render_template("viewInstructors.html",instructors=instructors,get_Department_by_tId=get_Department_by_tId)


def get_Department_by_tId(department_id):
    cursor.execute("select * from department where department_id='"+str(department_id)+"'")
    department = cursor.fetchall()
    department = department[0]
    return department


@app.route("/addSalary")
def addSalary():
    instructor_id = request.args.get("instructor_id")
    return render_template("addSalary.html",instructor_id=instructor_id)

@app.route("/addSalary1",methods=['post'])
def addSalary1():
    salary = request.form.get("salary")
    year = request.form.get("year")
    month = request.form.get("month")
    instructor_id = request.form.get("instructor_id")
    a = cursor.execute("select * from salaries where instructor_id='"+str(instructor_id)+"' and month='"+str(month)+"' and salary='"+str(salary)+"'")
    try:
        if a == 0:
            cursor.execute("insert into salaries(salary,year,month,instructor_id) values('"+str(salary)+"','"+str(year)+"','"+str(month)+"','"+str(instructor_id)+"')")
            conn.commit()
            return render_template("message.html", msg='Salary Added', color='alert-success')
        else:
            return render_template("message.html", msg='Salary Already Deposited In this  '+month+' '+year+'', color='alert-danger')
    except Exception as e:
        print(e)
        return render_template("message.html", msg='Something Went Wrong', color='alert-danger')


@app.route("/viewSalaries")
def viewSalaries():
    instructor_id = request.args.get("instructor_id")
    cursor.execute("select * from salaries where instructor_id='"+str(instructor_id)+"'")
    salaries = cursor.fetchall()
    return render_template("viewSalaries.html",salaries=salaries)

@app.route("/addSubject")
def addSubject():
    cursor.execute("select * from department")
    departments = cursor.fetchall()
    return render_template("addSubject.html",departments=departments)


@app.route("/addSubject1",methods=['post'])
def addSubject1():
    subject_name = request.form.get("subject_name")
    subject_code = request.form.get("subject_code")
    department_id = request.form.get("department_id")
    a = cursor.execute("select * from subjects where subject_code='"+str(subject_code)+"'")
    if a > 0:
        return render_template("message.html",msg='Subject Code Exits '+str(subject_code)+'',color='alert-danger')
    try:
       cursor.execute("insert into subjects(subject_name,subject_code,department_id) values('"+str(subject_name)+"','"+str(subject_code)+"','"+str(department_id)+"')")
       conn.commit()
       return render_template("message.html", msg='Subject Added Successfully', color='alert-success')
    except Exception as e:
        print(e)
        return render_template("message.html",msg='Something Went Wrong',color='alert-danger')



@app.route("/viewSubjects")
def viewSubjects():
    cursor.execute("select * from department")
    departments = cursor.fetchall()
    return render_template("viewSubjects.html",departments=departments)


def get_department_by_subject(department_id):
    cursor.execute("select * from department where department_id='"+str(department_id)+"'")
    department = cursor.fetchall()
    department = department[0]
    return department


@app.route("/viewDepartmentWiseSubjects")
def viewDepartmentWiseSubjects():
    department_id = request.args.get("department_id")
    cursor.execute("select * from subjects where department_id ='"+str(department_id)+"'")
    subjects = cursor.fetchall()
    if len(subjects) == 0:
        return render_template("message.html",msg='Subjects Not Found',color='alert-warning')
    return render_template("viewDepartmentWiseSubjects.html",subjects=subjects)


@app.route("/iLogin1",methods=['post'])
def iLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    a = cursor.execute("select * from instructor where email='" + str(email) + "' and password='" + str(password) + "'")
    details = cursor.fetchall()
    if a > 0:
        instructor = details[0]
        session['instructor_id'] = instructor[0]
        session['role'] = 'instructor'
        return render_template("instructor.html")
    else:
        return render_template("message.html", msg="Invalid Login Details", color='alert-danger')

@app.route("/instructor")
def instructor():
    return render_template("instructor.html")


@app.route("/studentRegistration")
def studentRegistration():
    cursor.execute("select * from department")
    departments = cursor.fetchall()
    return render_template("studentRegistration.html",departments=departments)


@app.route("/studentRegistration1",methods=['post'])
def studentRegistration1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    roll_number = request.form.get("roll_number")
    department_id = request.form.get("department_id")
    a = cursor.execute("select * from student where roll_number='"+str(roll_number)+"'")
    if a > 0:
        return render_template("message.html",msg='Roll Number Exits '+roll_number+'',color='alert-danger')
    try:
        cursor.execute("insert into student(name,email,phone,password,roll_number,department_id) values('" + str(
            name) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "','" + str(
            roll_number) + "','" + str(department_id) + "')")
        conn.commit()
        return render_template("message.html", msg='Student Registered Successfully', color='alert-success')
    except Exception as e:
        print(e)
        return render_template("message.html", msg='Something Went Wrong', color='alert-danger')



@app.route("/sLogin1",methods=['post'])
def sLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    a = cursor.execute("select * from student where email='" + str(email) + "' and password='" + str(password) + "'")
    details = cursor.fetchall()
    if a > 0:
        student = details[0]
        if student[6] == 'authorized':
            session['student_id'] = student[0]
            session['role'] = 'student'
            return render_template("student.html")
        else:
            return render_template("message.html",msg='Your Account Is UnAuthorized',color='alert-warning')
    else:
        return render_template("message.html", msg="Invalid Login Details", color='alert-danger')

@app.route("/viewStudents")
def viewStudents():
    cursor.execute("select * from student")
    students = cursor.fetchall()
    if len(students) == 0:
        return render_template("message.html",msg='Students Not Found',color='alert-info')
    return render_template("viewStudents.html",students=students,get_department_by_studentId=get_department_by_studentId)


def get_department_by_studentId(department_id):
    cursor.execute("select * from department")
    department = cursor.fetchall()
    department = department[0]
    return department


@app.route("/student_status",methods=['post'])
def student_status():
    student_id = request.form.get("student_id")
    cursor.execute("select * from student where student_id='" + str(student_id) + "'")
    details = cursor.fetchall()
    student = details[0]
    query = ""
    if student[6] == 'unauthorized':
        query = "update student set status='authorized' where student_id='" + str(student_id) + "'"

    else:
        query = "update student set status='unauthorized' where student_id='" + str(student_id) + "'"
    cursor.execute(query)
    conn.commit()
    return redirect("/viewStudents")

@app.route("/addSection")
def addSection():
    cursor.execute("select * from subjects where department_id in (select department_id from instructor where instructor_id='"+str(session['instructor_id'])+"')")
    subjects = cursor.fetchall()
    print(subjects)
    return render_template("addSection.html",subjects=subjects)


@app.route("/addSection1",methods=['post'])
def addSection1():
    crn_number = request.form.get("crn_number")
    room_number = request.form.get("room_number")
    number_of_students = request.form.get("number_of_students")
    subject_id = request.form.get("subject_id")
    weekday = request.form.get("weekday")
    class_time = request.form.get("class_time")
    section_fee = request.form.get("section_fee")

    cursor.execute("select * from section where instructor_id='" + str(session['instructor_id']) + "' and weekday='" + str(weekday) + "'")
    sections = cursor.fetchall()
    if len(sections) > 0:
        new_start_time = str(datetime.datetime.now().date()) + " " + str(class_time)
        new_start_time = datetime.datetime.strptime(new_start_time, "%Y-%m-%d %H:%M")
        new_end_time = new_start_time + datetime.timedelta(hours=2)
        cursor.execute("select * from section where instructor_id='"+str(session['instructor_id'])+"' and weekday='"+str(weekday)+"'")
        sections = cursor.fetchall()
        if len(sections) > 0:
            for section in sections:
                old_start_time = str(datetime.datetime.now().date()) + " " + str(section[4])
                old_start_time = datetime.datetime.strptime(old_start_time, "%Y-%m-%d %H:%M")
                old_end_time = old_start_time + datetime.timedelta(hours=2)
                if ((new_start_time >= old_start_time and new_start_time <= old_end_time) and (
                        new_end_time >= old_start_time and new_end_time >= old_end_time)):
                    return render_template("message.html", msg='You Have Time Conflict with Another Section. You can not Add This Section', color='alert-info')

                elif ((new_start_time <= old_start_time and new_start_time <= old_end_time) and (
                        new_end_time >= old_start_time and new_end_time <= old_end_time)):
                    return render_template("message.html", msg='You Have Time Conflict with Another Section. You can not Add This Section', color='alert-info')

                elif ((new_start_time >= old_start_time and new_start_time >= old_end_time) and (
                        new_end_time <= old_start_time and new_end_time <= old_end_time)):
                    return render_template("message.html", msg='You Have Time Conflict with Another Section. You can not Add This Section', color='alert-info')

                elif ((new_start_time >= old_start_time and new_start_time <= old_end_time) and (
                        new_end_time >= old_start_time and new_end_time <= old_end_time)):
                    return render_template("message.html", msg='You Have Time Conflict with Another Section. You can not Add This Section', color='alert-info')
    cursor.execute("insert into section(room_number,weekday,crn_number,class_time,number_of_students,section_fee,subject_id,instructor_id) values('"+str(room_number)+"','"+str(weekday)+"','"+str(crn_number)+"','"+str(class_time)+"','"+str(number_of_students)+"','"+str(section_fee)+"','"+str(subject_id)+"','"+str(session['instructor_id'])+"')")
    conn.commit()
    return render_template("message.html", msg='Section Added', color='alert-success')



@app.route("/viewSection")
def viewSection():
    search_result = request.args.get("search_result")
    query = ""
    if session['role'] == 'instructor':
        query = "select * from section where instructor_id='"+str(session['instructor_id'])+"'"
    elif session['role'] == 'student':
        if search_result == None:
            query = "select * from section where instructor_id in (select instructor_id from instructor where department_id in (select department_id from student where student_id='"+str(session['student_id'])+"'))"
        else:
            query = "select * from section where instructor_id in (select instructor_id from instructor where department_id in (select department_id from student where student_id='"+str(session['student_id'])+"')) and crn_number = '"+str(search_result)+"' or  instructor_id in (select instructor_id from instructor where name like'%" + str(search_result) + "%') or subject_id in (select subject_id from subjects where subject_name like'%" + str(search_result) + "%')"
    elif session['role'] == 'admin':
        query = "select * from section"
    cursor.execute(query)
    sections = cursor.fetchall()
    if len(sections) == 0:
        return render_template("message.html",msg='Results Not Found',color='alert-warning')
    return render_template("viewSection.html",isEnrolled=isEnrolled,search_result=search_result,get_instructor_by_section=get_instructor_by_section,sections=sections,get_subject_by_SectionId=get_subject_by_SectionId,get_department_by_subject=get_department_by_subject)



def get_subject_by_SectionId(subject_id):
    cursor.execute("select * from subjects where subject_id='"+str(subject_id)+"'")
    subject = cursor.fetchall()
    subject = subject[0]
    return subject

def get_instructor_by_section(instructor_id):
    cursor.execute("select * from instructor where instructor_id='"+str(instructor_id)+"' ")
    instructor = cursor.fetchall()
    instructor = instructor[0]
    return instructor

@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/enroll",methods=['post'])
def enroll():
    section_id = request.form.get("section_id")
    cursor.execute("select * from section where section_id='" + str(section_id) + "'")
    sections = cursor.fetchall()
    new_start_time = str(datetime.datetime.now().date()) + " " + sections[0][4]
    new_start_time = datetime.datetime.strptime(new_start_time, "%Y-%m-%d %H:%M")
    new_end_time = new_start_time + datetime.timedelta(hours=2)
    cursor.execute("select * from section where section_id!='" + str(section_id) + "' and weekday='" + str(sections[0][2]) + "' and section_id in (select section_id from enrollments where student_id='" + str(session['student_id']) + "' and (status='enrolled' or status='completed'))")
    sections = cursor.fetchall()
    if len(sections) > 0:
        for section in sections:
            old_start_time = str(datetime.datetime.now().date()) + " " + section[4]
            old_start_time = datetime.datetime.strptime(old_start_time, "%Y-%m-%d %H:%M")
            old_end_time = old_start_time + datetime.timedelta(hours=2)
            if ((new_start_time >= old_start_time and new_start_time <= old_end_time) and (
                    new_end_time >= old_start_time and new_end_time >= old_end_time)):
                return render_template("message.html", msg='You Have Time Conflict with Another Section. You can not Enroll This Section', color='alert-info')
            elif ((new_start_time <= old_start_time and new_start_time <= old_end_time) and (
                    new_end_time >= old_start_time and new_end_time <= old_end_time)):
                return render_template("message.html",msg='You Have Time Conflict with Another Section. You can not Enroll This Section',color='alert-info')


            elif ((new_start_time >= old_start_time and new_start_time >= old_end_time) and (
                    new_end_time <= old_start_time and new_end_time <= old_end_time)):
                return render_template("message.html",msg='You Have Time Conflict with Another Section. You can not Enroll This Section',color='alert-info')


            elif ((new_start_time >= old_start_time and new_start_time <= old_end_time) and (
                    new_end_time >= old_start_time and new_end_time <= old_end_time)):
                return render_template("message.html",msg='You Have Time Conflict with Another Section. You can not Enroll This Section',color='alert-info')

    cursor.execute("insert into enrollments (section_id,student_id) values('"+str(section_id)+"','"+str(session['student_id'])+"')")
    conn.commit()
    return render_template("message.html",msg='Section Enrolled',color='alert-success')



@app.route("/viewEnrollments")
def viewEnrollments():
    query = ""
    if session['role'] == 'instructor':
        section_id = request.args.get("section_id")
        query = "select * from enrollments where section_id='"+str(section_id)+"' and status='enrolled'"
    elif session['role'] == 'admin':
        section_id = request.args.get("section_id")
        query = "select * from enrollments where section_id='" + str(section_id) + "' and status='enrolled'"
    elif session['role'] == 'student':
        query = "select * from enrollments where student_id='"+str(session['student_id'])+"' and status='enrolled' "
    cursor.execute(query)
    enrollments = cursor.fetchall()
    if len(enrollments) == 0:
        return render_template("message.html",msg='No Enrollment')
    return render_template("viewEnrollments.html",int=int,getStudent_by_enrollment=getStudent_by_enrollment, get_instructor_by_section=get_instructor_by_section, get_subject_by_SectionId=get_subject_by_SectionId,get_department_by_subject=get_department_by_subject, enrollments=enrollments, get_section_by_enrollment=get_section_by_enrollment)


def getStudent_by_enrollment(student_id):
    cursor.execute("select * from student where student_id='"+str(student_id)+"'")
    student = cursor.fetchall()
    student = student[0]
    return student

def get_section_by_enrollment(section_id):
    cursor.execute("select * from section where section_id='"+str(section_id)+"'")
    sections = cursor.fetchall()
    section = sections[0]
    return section

def isEnrolled(section_id):
    a = cursor.execute("select * from enrollments where section_id='"+str(section_id)+"' and student_id='"+str(session['student_id'])+"' and status='enrolled'")
    if a == 0:
        return True
    else:
        return False


@app.route("/drop",methods=['post'])
def drop():
    enrollment_id = request.form.get("enrollment_id")
    cursor.execute("update enrollments set status ='dropped' where enrollment_id='"+str(enrollment_id)+"'")
    conn.commit()
    return redirect('/viewEnrollments')


@app.route("/payAmount",methods=['post'])
def payAmount():
    fee_paid = request.form.get("fee_paid")
    enrollment_id = request.form.get("enrollment_id")
    section_fee = request.form.get("section_fee")
    return render_template("payAmount.html",enrollment_id=enrollment_id,section_fee=section_fee,int=int,fee_paid=fee_paid)

@app.route("/payAmount1",methods=['post'])
def payAmount1():
    enrollment_id = request.form.get("enrollment_id")
    section_fee = request.form.get("section_fee")
    paid_amount = request.form.get("paid_amount")
    fee_paid = paid_amount
    cursor.execute("update enrollments set fee_paid = fee_paid +'"+str(fee_paid)+"' where enrollment_id='"+str(enrollment_id)+"'")
    conn.commit()
    cursor.execute("insert into transactions(paid_amount,enrollment_id) values('"+str(paid_amount)+"','"+str(enrollment_id)+"')")
    conn.commit()
    return render_template("message.html",msg='Amount Paid',color='alert-success')

@app.route("/viewTransactions",methods=['post'])
def viewTransactions():
    enrollment_id = request.form.get("enrollment_id")
    cursor.execute("select * from transactions where enrollment_id='"+str(enrollment_id)+"'")
    transactions = cursor.fetchall()
    if len(transactions) == 0:
        return render_template("message.html",msg='Transactions Not Available',color='alert-primary')
    return render_template("viewTransactions.html",transactions=transactions)


@app.route("/viewEnrollmentsHistory")
def viewEnrollmentsHistory():
    cursor.execute("select * from enrollments where student_id='"+str(session['student_id'])+"' and status='dropped' ")
    enrollments = cursor.fetchall()
    return render_template("viewEnrollmentsHistory.html",enrollments=enrollments,getStudent_by_enrollment=getStudent_by_enrollment,get_section_by_enrollment=get_section_by_enrollment,get_instructor_by_section=get_instructor_by_section,get_subject_by_SectionId=get_subject_by_SectionId,get_department_by_subject=get_department_by_subject)


@app.route("/giveGrade",methods=['post'])
def giveGrade():
    enrollment_id = request.form.get("enrollment_id")
    return render_template("giveGrade.html",enrollment_id=enrollment_id)


@app.route("/giveGrade1",methods=['post'])
def giveGrade1():
    grade = request.form.get("grade")
    attendance = request.form.get("attendance")
    enrollment_id = request.form.get("enrollment_id")
    cursor.execute("update enrollments set grade='"+str(grade)+"',attendance='"+str(attendance)+"' where enrollment_id='"+str(enrollment_id)+"'")
    conn.commit()
    return render_template("message.html",msg='Grade Given To Student',color='alert-success')

# app.run(debug=True)
app.run(host="0.0.0.0",port=50,debug=True)