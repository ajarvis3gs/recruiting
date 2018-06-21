# Choices used for M2M tables are actually not used in
# varChar fields. They must be manually inserted into db.

import pytz
from django_countries import countries

TIMEZONE_CHOICES = tuple((choice, choice) for choice in pytz.common_timezones)

COUNTRY_CHOICES = tuple(countries)

CANDIDATE_STATUS_CHOICES = (
    ('New', 'New'),
    ('Contacted', 'Contacted'),
    ('Awaiting Response Form', 'Awaiting Response Form'),
    ('Response Form Completed', 'Response Form Completed'),
    ('Awaiting Interview', 'Awaiting Interview'),
    ('Interview Completed', 'Interview Completed'),
    ('Additional Information Requested', 'Additional Information Requested'),
    ('Not Submitted - Inexperienced', 'Not Submitted - Inexperienced'),
    ('Not Submitted - Unqualified', 'Not Submitted - Unqualified'),
    ('Not Submitted - Position Filled', 'Not Submitted - Position Filled'),
    ('Submitted', 'Submitted'),
)

GENDER_CHOICES = (
    ('', ''),
    ('male', 'Male'),
    ('female', 'Female'),
)

EDUCATION_CHOICES = (
    ('', ''),
    ('High School', 'High School'),
    ('Vocational School', 'Vocational School'),
    ('Community College', 'Community College'),
    ("Bachelor's Degree", "Bachelor's Degree"),
    ("Master's Degree", "Master's Degree"),
    ('MBA', 'MBA'),
    ('PhD', 'PhD'),
)

EMPLOYER_TYPE_CHOICES = (
    ('University', 'University'),
    ('High School', 'High School'),
    ('Middle School', 'Middle School'),
    ('Primary School', 'Primary School'),
    ('Kindergarten', 'Kindergarten'),
    ('Youth Language Center', 'Youth Language Center'),
    ('Adult Language Center', 'Adult Language Center'),
)

POSITION_TYPE_CHOICES = (
    ('Teacher', 'Teacher'),
    ('Manager', 'Manager'),
    ('Principal', 'Principal'),
    ('Partner', 'Partner'),
)

DESIRED_MONTHLY_SALARY_CHOICES = (
    ('1000', '1000+'),
    ('2000', '2000+'),
    ('3000', '3000+'),
    ('4000', '4000+'),
    ('5000', '5000+'),
    ('6000', '6000+'),
    ('7000', '7000+'),
    ('8000', '8000+'),
    ('9000', '9000+'),
    ('10000', '10000+'),
    ('11000', '11000+'),
    ('12000', '12000+'),
    ('13000', '13000+'),
    ('14000', '14000+'),
    ('15000', '15000+'),
    ('16000', '16000+'),
    ('17000', '17000+'),
    ('18000', '18000+'),
    ('19000', '19000+'),
    ('20000', '20000+'),
    ('21000', '21000+'),
    ('22000', '22000+'),
    ('23000', '23000+'),
    ('24000', '24000+'),
    ('25000', '25000+'),
)

REGION_CHOICES = (
    ('', ''),
    (1, 'Default Region'),
    (2, 'Mid-Hudson Region'),
    (3, 'NYC Metro Region'),
)

SERVICE_GROUP_CHOICES = (
    ('', ''),
    (1, 'Standard Titles'),
    (2, 'Software/Hardware Specific Titles'),
)

JOB_TITLE_CHOICES = (
    ('', ''),
    ('Ansible Specialist', 'Ansible Specialist'),
    ('Senior Java Developer', 'Senior Java Developer'),
    ('Python/Django Developer', 'Python/Django Developer'),
    ('MDE Altassian Product Administrator', 'MDE Altassian Product Administrator'),
    ('MDE Release Coordinator', 'MDE Release Coordinator'),
    ('MDE Tools Admin', 'MDE Tools Admin'),
    ('Senior Cloud Systems/DevOps Engineer', 'Senior Cloud Systems/DevOps Engineer'),
    ('Business Analyst', 'Business Analyst'),
    ('Project Manager', 'Project Manager'),
    ('Tester', 'Tester'),
    ('Programmer', 'Programmer'),
    ('Technical Architect', 'Technical Architect'),
    ('Technical Writer', 'Technical Writer'),
    ('Specialist', 'Specialist'),
    ('System Administrator', 'System Administrator'),
    ('Database Administrator', 'Database Administrator'),
    ('Technician V', 'Technician V'),
    ('Principal Consultant', 'Principal Consultant'),
    ('Technical Specialist 3', 'Technical Specialist 3'),
    ('Technical Specialist 4', 'Technical Specialist 4'),
    ('Technical Specialist 5', 'Technical Specialist 5'),
    ('Software Architect #1', 'Software Architect #1'),
    ('Software Architect #2', 'Software Architect #2'),
    ('Architectural Specialist I', 'Architectural Specialist I'),
    ('Architectural Specialist II', 'Architectural Specialist II'),
    ('Sr. Production Control Operator', 'Sr. Production Control Operator'),
    ('Production Control Operator', 'Production Control Operator'),
    ('Sr. Equipment Operator', 'Sr. Equipment Operator'),
    ('Equipment Operator', 'Equipment Operator'),
    ('Service Delivery Specialist I', 'Service Delivery Specialist I'),
    ('Service Delivery Specialist II', 'Service Delivery Specialist II'),
)

EXPERIENCE_LEVEL_CHOICES = (
    ('', 'Any'),
    ('Junior', 'Junior (12-36 Months)'),
    ('Mid Level', 'Mid Level (36-60 Months)'),
    ('Senior', 'Senior (60-84 Months)'),
    ('Expert', 'Expert (84+ Months)'),
)

DEMAND_CHOICES = (
    ('', 'Any'),
    ('High', 'High'),
    ('Normal', 'Normal'),
)

FILE_TYPE_CHOICES = (
    ('', 'Other'),
    ('Task Order Form', 'Task Order Form'),
    ('Candidate Response Form', 'Candidate Response Form'),
)