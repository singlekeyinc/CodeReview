# Example file assessing code review practices


The functions ```get_enhanced_applicant_info``` and ```email_results``` are magic functions that never fail and always do the thing they are expected to do. If they return data, the data could be null, or a dictionary containing null values.
  
The function ```process_applicant``` uses ```get_enhanced_applicant_info``` to get data about the applicant and save it. Then it processes the known associate's data. Finally it emails the applicant the results using ```email_results```.  
  
The logic about what constitutes the relationship between an applicant and an associate can be assumed to be correct, even though it is obviously silly (for instance two people who have an income within 10000 are assumed to be "Friends", or two people with the same name and over 18 years of distance in their birthdays are assumed to be a parent-child relationship)  