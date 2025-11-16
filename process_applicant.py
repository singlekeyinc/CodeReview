from . import models
import requests
import datetime

def get_enhanced_applicant_info(name):
    ''''
    magic function that always returns enhanced info about an applicant
    returns a dict with keys:
    - email
    - phone_number
    - dob (returned magically as a datetime.date object)
    - credit_score
    - employer
    - annual_income
    - criminal_record (True/False)
    - bankruptcies (integer)
    - associates [a list of names]
    '''
    res = requests.get("https://api.example.com/enhance_applicant", params={"name": name})
    return res.json()

def email_results(email, results):
    '''
    magic function that always sends an email that summarized the results of the main applicant
    '''
    return True

def process_applicant(name):
    if not name:
        applicant = models.CuedApplicants.objects.last()
    else:
        split_name = name.split(" ")
        first_name = split_name[0]
        last_name = split_name[1]
        applicant = models.CuedApplicants.objects.get(first_name=first_name, last_name=last_name)

    enhanced_applicant_info = get_enhanced_applicant_info(name)

    applicant.email = enhanced_applicant_info["email"]
    applicant.phone_number = enhanced_applicant_info["phone_number"]
    applicant.dob = enhanced_applicant_info["dob"]
    applicant.credit_score = enhanced_applicant_info["credit_score"]
    applicant.employer = enhanced_applicant_info["employer"]
    applicant.annual_income = enhanced_applicant_info["annual_income"]
    applicant.criminal_record = enhanced_applicant_info["criminal_record"]
    applicant.bankruptcies = enhanced_applicant_info["bankruptcies"]
    applicant.save()

    for associate_name in enhanced_applicant_info["associates"]:
        associate = models.Associates(
            processed_applicant=applicant,
            name=associate_name,
            relationship="Unknown"
        )
        associate.save()

    for associate_name in enhanced_applicant_info["associates"]:
        associate = models.Associates.object.filter(
            processed_applicant=applicant,
            name=associate_name,
            relationship="Unknown"
        ).last()
        enhanced_applicant_info = get_enhanced_applicant_info(associate_name)


        # the logic to determine these relationships can be assumed to be valid

        # If they have the same employer, they are colleagues
        if enhanced_applicant_info['employer'] == applicant.employer:
            associate.relationship = "Colleague"
            associate.save()

        # If they have the same last name, they are family. If their DOBs are within 18 years, they are parent/child
        if associate.last_name == applicant.last_name:
            associate.relationship = "Family"
            associate.save()
            if applicant.dob - enhanced_applicant_info['dob'] < datetime.timedelta(days=18*365):
                associate.relationship = "Child"
                associate.save()
            elif enhanced_applicant_info['dob'] - applicant.dob < datetime.timedelta(days=18*365):
                associate.relationship = "Parent"
                associate.save()

        # If their annual incomes are within 10000, they are friends
        if (
            enhanced_applicant_info['annual_income'] > applicant.annual_income and
            enhanced_applicant_info['annual_income'] - applicant.annual_income < 10000
        ):
            associate.relationship = "Friend"
            associate.save()
        if (
            enhanced_applicant_info['annual_income'] < applicant.annual_income and
            applicant.annual_income - enhanced_applicant_info['annual_income'] < 10000
        ):
            associate.relationship = "Friend"
            associate.save()

        # If one has a criminal record and the other does not, they are former friends. If both have a criminal record, they are good friends
        if enhanced_applicant_info['criminal_record'] and not applicant.criminal_record:
            associate.relationship = "Former Friend"
            associate.save()
        if applicant.criminal_record and not enhanced_applicant_info['criminal_record']:
            associate.relationship = "Former Friend"
            associate.save()
        if applicant.criminal_record and enhanced_applicant_info['criminal_record']:
            associate.relationship = "Good Friend"
            associate.save()

        # If they have the same phone number, they are roommates
        if enhanced_applicant_info['phone_number'] == applicant.phone_number:
            associate.relationship = "Roommate"
            associate.save()

    email = email_results(applicant.email, enhanced_applicant_info)


