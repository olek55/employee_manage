# Generated by Django 5.0.1 on 2024-03-18 12:42

import django.db.models.deletion
import markdownx.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country_management', '0020_alter_currency_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='country',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='country',
        ),
        migrations.RemoveField(
            model_name='country',
            name='workforce_description',
        ),
        migrations.AlterField(
            model_name='employeebenefitsandentitlements',
            name='health_insurance_requirements',
            field=markdownx.models.MarkdownxField(help_text='Examine the health insurance requirements for employees in [Country], discussing statutory provisions, employer obligations, and options for additional coverage. Embed credible sources directly within the guide. Organize the content with H2 headings, focusing on delivering practical and detailed information succinctly.'),
        ),
        migrations.AlterField(
            model_name='employeebenefitsandentitlements',
            name='mandatory_benefits',
            field=markdownx.models.MarkdownxField(help_text='Provide a comprehensive overview of mandatory employee benefits in [Country], such as social security, health insurance, and pension contributions. Include authoritative sources within the text to lend credibility. Structure the guide starting with H2 headings, aiming for a focused and detailed exposition without needing introductory or concluding remarks.'),
        ),
        migrations.AlterField(
            model_name='employeebenefitsandentitlements',
            name='optional_benefits',
            field=markdownx.models.MarkdownxField(help_text='Detail the optional employee benefits commonly offered by employers in [Country], including but not limited to, private health insurance, gym memberships, and stock options. Integrate relevant references into the content for factual support. Use H2 headings to structure the guide, presenting a clear and actionable overview without the need for preambles or summaries.'),
        ),
        migrations.AlterField(
            model_name='employeebenefitsandentitlements',
            name='retirement_plans',
            field=markdownx.models.MarkdownxField(help_text='Explore the retirement plans available to employees in [Country], including government-sponsored pensions and private savings options. Incorporate authoritative references to support the discussion. Structure the information from H2 headings, ensuring the guide is direct and informative, devoid of unnecessary introductions or conclusions.'),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='employee_tax_deductions',
            field=markdownx.models.MarkdownxField(help_text='Detail the employee tax deductions in [Country], covering types, eligibility criteria, and calculation methods. Embed relevant references within the text to enhance credibility. Use H2 headings to structure the guide, aiming for a direct, informative approach without introductory or concluding sections.'),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='employer_tax_responsibilites',
            field=markdownx.models.MarkdownxField(help_text='Outline the employer tax responsibilities in [Country], including rates, categories, and payment deadlines. Ensure authoritative resources are integrated within the guide to provide verification. Structure the content with H2 headings from the outset, focusing on delivering a clear and detailed guide without the need for opening or closing remarks.'),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='tax_incentives',
            field=markdownx.models.MarkdownxField(help_text='Explore the tax incentives available to businesses in [Country], including types, qualification criteria, and application processes. Incorporate relevant sources within the guide for factual accuracy. Begin with H2 headings for structure, ensuring the content is straightforward and actionable.'),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='vat',
            field=markdownx.models.MarkdownxField(help_text='Examine the Value-Added Tax (VAT) implications for services in [Country], discussing rates, exemptions, and filing procedures. Integrate authoritative sources directly into the content for substantiation. Organize the information starting with H2 headings, presenting the details concisely and efficiently.'),
        ),
        migrations.CreateModel(
            name='CountryOverview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_description', markdownx.models.MarkdownxField(help_text='Provide an in-depth overview of [Country], covering geographical, historical, and socio-economic aspects. Integrate authoritative sources directly into the narrative to support your descriptions. Organize the content starting with H2 headings, and ensure the guide is comprehensive, yet direct, without the need for an introductory or concluding section.')),
                ('workforce_description', markdownx.models.MarkdownxField(help_text='Detail the characteristics of the workforce in [Country], including demographics, skill levels, and sectoral distribution. Embed relevant statistics and findings from credible sources within the content. Use H2 headings as your structural guide to deliver a clear, detailed analysis without introductory or concluding remarks.')),
                ('cultural_norms_impacting_employment', markdownx.models.MarkdownxField(help_text='Examine the cultural norms in [Country] that influence employment practices, including work-life balance, communication styles, and organizational hierarchies. Incorporate insights from reputable sources to enrich the guide. Content should be structured starting from H2 headings, focusing on delivering actionable insights directly.')),
                ('key_industries_and_employment_sectors', markdownx.models.MarkdownxField(help_text='Explore the key industries and employment sectors driving the economy in [Country], highlighting emerging sectors and those with significant employment. Include up-to-date references within the text to substantiate your points. Structure the guide with H2 headings, aiming for a straightforward presentation of facts without preamble or closure.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='overview', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Country Overview',
                'verbose_name_plural': 'Country Overviews',
            },
        ),
        migrations.CreateModel(
            name='CulturalConsiderations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication_styles_in_the_workplace', markdownx.models.MarkdownxField(help_text='Detail the prevalent communication styles in the workplace in [Country], including directness, formality, and the role of non-verbal cues. Embed relevant cultural studies and business practices within the text to offer depth. Organize the content with H2 headings, aiming for a guide that provides actionable insights without the need for an introduction or conclusion.')),
                ('negotiation_practices', markdownx.models.MarkdownxField(help_text='Examine negotiation practices in [Country], focusing on approaches, typical strategies, and cultural norms that influence business dealings. Integrate authoritative references to enhance credibility. Structure the guide starting from H2 headings, offering a clear and thorough exploration of negotiation nuances.')),
                ('understanding_hierarchical_structures', markdownx.models.MarkdownxField(help_text='Explore the hierarchical structures prevalent in businesses in [Country], including the impact on decision-making, team dynamics, and leadership styles. Incorporate insights from cultural analysis and management theories directly into the content. Begin with H2 headings for a structured, informative guide.')),
                ('holidays_and_observances_affecting_business_operations', markdownx.models.MarkdownxField(help_text='Describe the major holidays and observances in [Country] that affect business operations, including statutory holidays, regional observances, and their impact on work schedules. Seamlessly embed cultural and legal references within the text. Use H2 headings to structure the content, focusing on practical implications for businesses.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cultural_considerations', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Cultural Considerations',
                'verbose_name_plural': 'Cultural Considerations',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='DisputeResolutionandLegalCompliance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('labor_courts_and_arbitration_panels', markdownx.models.MarkdownxField(help_text='Examine the structure and function of labor courts and arbitration panels in [Country], including their jurisdiction, process, and typical cases handled. Integrate relevant legal sources to provide a comprehensive overview. Structure the guide with H2 headings, focusing on delivering clear and actionable insights without introductory or concluding sections.')),
                ('compliance_audits_and_inspections', markdownx.models.MarkdownxField(help_text='Detail the procedures and importance of compliance audits and inspections in [Country], covering who conducts them, frequency, and the consequences of non-compliance. Embed authoritative references within the text to ensure accuracy. Use H2 headings to organize the content, aiming for a direct and thorough exposition.')),
                ('reporting_and_whistleblower_protections', markdownx.models.MarkdownxField(help_text='Discuss the mechanisms for reporting violations and the protections in place for whistleblowers in [Country], highlighting legal provisions and practical considerations. Incorporate credible legal and regulatory references directly into the guide for substantiation. Structure the content starting with H2 headings, providing comprehensive and practical guidance.')),
                ('international_labor_standards_compliance', markdownx.models.MarkdownxField(help_text='Explore how [Country] complies with international labor standards, including adherence to conventions and treaties, and the impact on domestic labor laws. Seamlessly integrate relevant international and local legal sources within the text. Begin with H2 headings for structure, ensuring the guide is informative and applicable.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dispute_resolution_and_legal_compliance', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Dispute Resolution and Legal Compliance',
                'verbose_name_plural': 'Dispute Resolution and Legal Compliance',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='EmploymentAgreements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types_of_employment_agreements', markdownx.models.MarkdownxField(help_text='Detail the various types of employment agreements in [Country], including permanent, temporary, part-time, and freelance contracts. Integrate relevant legal sources within the text to provide accuracy. Organize the content starting with H2 headings, focusing on delivering comprehensive insights without introductory or concluding remarks.')),
                ('essential_clauses', markdownx.models.MarkdownxField(help_text='Examine the essential clauses that should be included in employment agreements in [Country], such as job description, compensation, working hours, and termination conditions. Embed authoritative references to support the discussion. Use H2 headings to structure the guide, ensuring it is informative and straightforward.')),
                ('probationary_period', markdownx.models.MarkdownxField(help_text='Explore the concept of the probationary period in employment agreements in [Country], covering typical durations, employee rights, and evaluation criteria. Incorporate credible sources directly into the guide for validation. Begin with H2 headings for structure, aiming for a clear and detailed exposition.')),
                ('confidentiality_and_non_compete_clauses', markdownx.models.MarkdownxField(help_text='Discuss the confidentiality and non-compete clauses in employment agreements in [Country], including scope, duration, and enforceability. Seamlessly integrate relevant legal sources within the text. Structure the content from H2 headings, providing a direct and actionable guide.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employment_agreements', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Employment Agreements',
                'verbose_name_plural': 'Employment Agreements',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='FreelancingandIndependentContracting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difference_employees_and_contractors', markdownx.models.MarkdownxField(help_text='Detail the legal distinctions between employees and independent contractors in [Country], focusing on contractual obligations, worker rights, and employer responsibilities. Integrate relevant legal references within the text to ensure accuracy. Organize the guide starting with H2 headings, providing clear and comprehensive insights without introductory or concluding remarks.')),
                ('independent_contracting', markdownx.models.MarkdownxField(help_text='Explore the nuances of independent contracting in [Country], including contract structures, negotiation practices, and common industries. Embed authoritative sources to substantiate the discussion. Use H2 headings to structure the content, aiming for a direct and thorough guide.')),
                ('intellectual_property_rights', markdownx.models.MarkdownxField(help_text='Examine intellectual property rights considerations for freelancers and independent contractors in [Country], covering copyright, patents, and trademarks as applicable. Incorporate credible legal sources directly into the text for validation. Structure the information from H2 headings, focusing on practical and detailed guidance.')),
                ('tax_and_insurance', markdownx.models.MarkdownxField(help_text='Describe the tax obligations and insurance options for freelancers and independent contractors in [Country], including necessary filings, deductions, and risk management strategies. Seamlessly integrate relevant tax legislation and insurance norms within the guide. Begin with H2 headings for organization, ensuring clarity and utility.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='freelancing_and_independent_contracting', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Freelancing and Independent Contracting',
                'verbose_name_plural': 'Freelancing and Independent Contracting',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='HealthandSafetyRequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_and_safety_laws', markdownx.models.MarkdownxField(help_text='Provide an in-depth overview of health and safety laws in [Country], covering key legislation, employer obligations, and employee rights. Embed relevant legal references within the text for accuracy. Structure the guide with H2 headings, focusing on essential information without the need for introductions or conclusions.')),
                ('occupational_health_and_safety', markdownx.models.MarkdownxField(help_text='Detail the standards and practices for occupational health and safety in [Country], including risk assessments, training requirements, and incident reporting. Incorporate authoritative sources directly into the content for substantiation. Use H2 headings to organize the guide, aiming for clear and actionable insights.')),
                ('workplace_inspection', markdownx.models.MarkdownxField(help_text='Examine the role and procedures for workplace inspections in [Country], highlighting inspection criteria, frequency, and follow-up actions. Seamlessly integrate relevant regulations and guidelines within the guide. Structure the content starting with H2 headings, providing a thorough and practical overview.')),
                ('workplace_accidents', markdownx.models.MarkdownxField(help_text='Discuss the protocols for dealing with workplace accidents in [Country], including reporting requirements, investigation processes, and compensation claims. Embed credible legal and regulatory references to support the discussion. Begin with H2 headings for the structure, focusing on delivering comprehensive and useful information.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='health_and_safety_requirements', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Health and Safety Requirements',
                'verbose_name_plural': 'Health and Safety Requirements',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='RemoteWorkandFlexibleWorkArrangements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_work', markdownx.models.MarkdownxField(help_text='Provide an in-depth analysis of remote work policies and practices in [Country], covering legal regulations, technological infrastructure requirements, and employer responsibilities. Integrate relevant laws and guidelines within the text to ensure accuracy. Structure the guide with H2 headings, focusing on concise yet comprehensive coverage without the need for introductory or concluding sections.')),
                ('flexible_work_arrangements', markdownx.models.MarkdownxField(help_text='Examine flexible work arrangements in [Country], including part-time work, flexitime, job sharing, and telecommuting. Detail the equipment and expense reimbursements policies, embedding applicable legal sources for verification. Use H2 headings to organize the content, aiming for a clear and actionable guide without preambles or summaries.')),
                ('data_protection_and_privacy', markdownx.models.MarkdownxField(help_text='Discuss data protection and privacy considerations for remote employees in [Country], highlighting employer obligations, employee rights, and best practices for securing personal and company data. Incorporate authoritative references to support the discussion. Structure the guide from H2 headings, delivering straightforward and relevant information.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='remote_work', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Remote Work and Flexible Work Arrangements',
                'verbose_name_plural': 'Remote Work and Flexible Work Arrangements',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='SalaryandCompensation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_competitive_salaries', markdownx.models.MarkdownxField(help_text='Analyze the concept of market competitive salaries in [Country], including factors influencing salary levels, sector-specific benchmarks, and trends in compensation. Integrate authoritative financial and employment resources within the content for substantiation. Structure the guide with H2 headings, aiming for a detailed exposition without the need for introductory or concluding remarks.')),
                ('minimum_wage', markdownx.models.MarkdownxField(help_text='Detail the minimum wage regulations in [Country], covering legal standards, sectoral variations, and adjustments for living costs. Embed relevant legislative references to ensure accuracy. Use H2 headings to organize the content, focusing on delivering practical and comprehensive insights.')),
                ('bonuses_and_allowances', markdownx.models.MarkdownxField(help_text='Explore the variety of bonuses and allowances offered to employees in [Country], such as performance bonuses, holiday pay, and travel allowances. Incorporate credible sources directly into the guide for validation. Begin structuring the content from H2 headings, providing clear and actionable guidance.')),
                ('payroll_cycle', markdownx.models.MarkdownxField(help_text='Examine the payroll cycle practices in [Country], including common pay periods, statutory requirements for payment timeliness, and variations by industry. Seamlessly integrate authoritative financial and legal references within the text. Structure the guide with H2 headings, ensuring it offers direct and useful information.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='salary_and_compensation', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Salary and Compensation',
                'verbose_name_plural': 'Salary and Compensation',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='StandardWorkingHoursandOvertime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard_working_hours', markdownx.models.MarkdownxField(help_text='Outline the regulations governing standard working hours in [Country], including legal limits, exceptions, and variations by sector or contract type. Integrate applicable legal references within the content to provide authoritative support. Use H2 headings to structure the guide, delivering comprehensive insights without introductory or concluding remarks.')),
                ('overtime', markdownx.models.MarkdownxField(help_text='Detail the rules and compensation for overtime work in [Country], covering eligibility, calculation methods, and maximum limits. Embed relevant legislation and guidelines to ensure accuracy. Organize the content starting with H2 headings, focusing on a clear and actionable exposition.')),
                ('rest_periods_and_breaks', markdownx.models.MarkdownxField(help_text='Examine the entitlements to rest periods and breaks for workers in [Country], including daily rest, meal breaks, and day-offs. Incorporate authoritative sources directly into the guide for verification. Begin structuring the content with H2 headings, aiming for direct and detailed guidance.')),
                ('night_shift_and_weekend_regulations', markdownx.models.MarkdownxField(help_text='Discuss the specific regulations for night shift and weekend work in [Country], such as premium pay rates, health and safety considerations, and opt-out rights. Seamlessly integrate applicable legal references within the text. Use H2 headings to organize the guide, ensuring it provides practical and comprehensive information.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='standard_working_hours', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Standard Working Hours and Overtime',
                'verbose_name_plural': 'Standard Working Hours and Overtime',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='Termination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_period', markdownx.models.MarkdownxField(help_text='Explain the legal requirements for notice periods in [Country] during employment termination, including variations by employee status and length of service. Embed relevant labor law references within the text for credibility. Structure the content from H2 headings, aiming to provide a detailed and actionable guide without the need for introductory or concluding sections.')),
                ('severance_pay', markdownx.models.MarkdownxField(help_text='Detail the severance pay entitlements in [Country], covering eligibility, calculation methods, and exceptions. Incorporate authoritative legal sources to substantiate the information presented. Use H2 headings to organize the guide, ensuring it is comprehensive and directly applicable.')),
                ('termination_process', markdownx.models.MarkdownxField(help_text='Describe the termination process in [Country], including procedural steps, documentation requirements, and employee rights. Seamlessly integrate applicable legal guidelines within the text for validation. Begin structuring the content with H2 headings, focusing on clarity and thoroughness.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='termination', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Termination and Severance',
                'verbose_name_plural': 'Termination and Severance',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='VacationandLeavePolicies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_leave', markdownx.models.MarkdownxField(help_text='Detail the vacation leave entitlements in [Country], including minimum leave requirements, accrual rates, and conditions for use. Integrate relevant labor laws and guidelines within the text to lend authority. Organize the content starting with H2 headings, focusing on delivering essential information without preliminary or summary remarks.')),
                ('public_holidays', markdownx.models.MarkdownxField(help_text='Explore the public holidays observed in [Country], noting any regional variations and the impact on employee leave entitlements. Embed authoritative sources to validate the information. Use H2 headings to structure the guide, aiming for a direct and comprehensive overview.')),
                ('types_of_leave', markdownx.models.MarkdownxField(help_text='Examine the various types of leave available to employees in [Country], such as sick leave, maternity/paternity leave, and unpaid leave. Incorporate credible legal and regulatory references directly into the guide for substantiation. Begin with H2 headings for organization, ensuring the content is practical and detailed.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vacation_and_leave', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Vacation and Leave Policies',
                'verbose_name_plural': 'Vacation and Leave Policies',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='WorkersRightsandProtections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termination', markdownx.models.MarkdownxField(help_text='Delve into the regulations surrounding the termination of employment in [Country], covering lawful grounds for dismissal, notice requirements, and severance pay. Ensure that authoritative resources are integrated within the text to support your discussion. Organize the content starting with H2 headings, offering a thorough guide without necessitating introductory or concluding sections.')),
                ('discrimination', markdownx.models.MarkdownxField(help_text='Detail the anti-discrimination laws in [Country], focusing on protected characteristics, redress mechanisms, and employer responsibilities. Embed credible sources directly into the content for validation. Use H2 headings as the basis for structure, aiming to provide a clear, actionable understanding without prefaces or summaries.')),
                ('working_conditions', markdownx.models.MarkdownxField(help_text='Explain the standards for working conditions in [Country], including work hours, rest periods, and ergonomic requirements. Incorporate relevant references within the guide to enhance reliability. Structure the information from H2 headings, creating a concise and informative guide devoid of general introductions or conclusions.')),
                ('health_and_safety', markdownx.models.MarkdownxField(help_text='Explore health and safety regulations in the workplace in [Country], discussing employer obligations, employee rights, and enforcement agencies. Seamlessly integrate authoritative sources to substantiate the information. Begin structuring the content with H2 headings, ensuring the guide is straightforward and informative.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workers_rights', to='country_management.country')),
            ],
            options={
                'verbose_name': 'Workers Rights and Protections',
                'verbose_name_plural': 'Workers Rights and Protections',
                'ordering': ['country'],
            },
        ),
        migrations.DeleteModel(
            name='Benefit',
        ),
        migrations.DeleteModel(
            name='Leave',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
