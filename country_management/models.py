from django.db import models
from markdownx.models import MarkdownxField
from .custom_fields import CustomMarkdownxField

# Create your models here.

# 1. Country


class Country(models.Model):
    name = models.CharField(max_length=512)
    slug = models.SlugField(max_length=512, unique=True, null=True, blank=True)
    capital = models.CharField(max_length=512)
    region = models.CharField(max_length=512)
    currency = models.ForeignKey(
        "Currency", on_delete=models.CASCADE, related_name="countries"
    )
    population = models.IntegerField()
    gdp_growth = models.FloatField(null=True, blank=True)
    gdp_share = models.FloatField(null=True, blank=True)
    flag = models.ImageField(upload_to="country_flags/", null=True, blank=True)
    image = models.ImageField(upload_to="country_images/", null=True, blank=True)
    holiday_code = models.CharField(max_length=128)
    land_code = models.CharField(max_length=128, blank=True, null=True)
    language = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    availability = models.BooleanField(default=True)

    class Meta:
        verbose_name = "A. Country"
        verbose_name_plural = "A. Countries"

    def __str__(self):
        return self.name


class Currency(models.Model):
    currency_code = models.CharField(max_length=512)
    currency_name = models.CharField(max_length=512)
    currency_symbol = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Z. Currency"
        verbose_name_plural = "Z. Currencies"

    def __str__(self):
        return self.currency_code


class Address(models.Model):
    address_line_1 = models.CharField(max_length=255, null=True, default="", blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, default="", blank=True)
    zip_code = models.CharField(max_length=255, null=True, default="", blank=True)
    city = models.CharField(max_length=255, null=True, default="", blank=True)
    state = models.CharField(max_length=255, null=True, default="", blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="country_name",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "P. Address"


# B. Country Overview
class CountryOverview(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="overview"
    )
    country_description = CustomMarkdownxField(
        help_text="Provide an in-depth overview of [Country], covering geographical, historical, and socio-economic aspects. Integrate authoritative sources directly into the narrative to support your descriptions. Return in markdown, start with H2 headings and use H3, H4 if needed and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    workforce_description = CustomMarkdownxField(
        help_text="Detail the characteristics of the workforce in [Country], including demographics, skill levels, and sectoral distribution. Embed relevant statistics and findings from credible sources within the content. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    cultural_norms_impacting_employment = CustomMarkdownxField(
        help_text="Examine the cultural norms in [Country] that influence employment practices, including work-life balance, communication styles, and organizational hierarchies. Incorporate insights from reputable sources to enrich the guide. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    key_industries_and_employment_sectors = CustomMarkdownxField(
        help_text="Explore the key industries and employment sectors driving the economy in [Country], highlighting emerging sectors and those with significant employment. Include up-to-date references within the text to substantiate your points. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "B. Country Overview"
        verbose_name_plural = "B. Country Overviews"


# 3. Tax Obligations


class TaxObligations(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="tax_obligations"
    )
    employer_tax_responsibilites = CustomMarkdownxField(
        help_text="Outline the employer tax responsibilities in [Country]. Ensure authoritative resources are integrated within the guide to provide verification. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    employee_tax_deductions = CustomMarkdownxField(
        help_text="Detail the employee tax deductions in [Country]. Embed relevant references within the text to enhance credibility. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    vat = CustomMarkdownxField(
        help_text="Examine the Value-Added Tax (VAT) implications for services in [Country]. Integrate authoritative sources directly into the content for substantiation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    tax_incentives = CustomMarkdownxField(
        help_text="Explore the tax incentives available to businesses in [Country]. Incorporate relevant sources within the guide for factual accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "C. Tax Obligations"
        verbose_name_plural = "C. Tax Obligations"


# 4. Employee Benefits and Entitlements
class EmployeeBenefitsAndEntitlements(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="employee_benefits"
    )
    mandatory_benefits = CustomMarkdownxField(
        help_text="Provide a comprehensive overview of mandatory employee benefits in [Country]. Include authoritative sources within the text to lend credibility. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    optional_benefits = CustomMarkdownxField(
        help_text="Detail the optional employee benefits commonly offered by employers in [Country]. Integrate relevant references into the content for factual support. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    health_insurance_requirements = CustomMarkdownxField(
        help_text="Examine the health insurance requirements for employees in [Country]. Embed credible sources directly within the guide. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    retirement_plans = CustomMarkdownxField(
        help_text="Explore the retirement plans available to employees in [Country]. Incorporate authoritative references to support the discussion. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "D. Benefits and Entitlements"
        verbose_name_plural = "D. Benefits and Entitlements"
        ordering = ["country"]


# 5. Workers Rights and Protections
class WorkersRightsandProtections(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="workers_rights"
    )
    termination = CustomMarkdownxField(
        help_text="Delve into the regulations surrounding the termination of employment in [Country], covering lawful grounds for dismissal, notice requirements, and severance pay. Ensure that authoritative resources are integrated within the text to support your discussion. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    discrimination = CustomMarkdownxField(
        help_text="Detail the anti-discrimination laws in [Country], focusing on protected characteristics, redress mechanisms, and employer responsibilities. Embed credible sources directly into the content for validation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    working_conditions = CustomMarkdownxField(
        help_text="Explain the standards for working conditions in [Country], including work hours, rest periods, and ergonomic requirements. Incorporate relevant references within the guide to enhance reliability. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    health_and_safety = CustomMarkdownxField(
        help_text="Explore health and safety regulations in the workplace in [Country], discussing employer obligations, employee rights, and enforcement agencies. Seamlessly integrate authoritative sources to substantiate the information. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "E. Rights and Protections"
        verbose_name_plural = "E. Rights and Protections"
        ordering = ["country"]


# 6. Employment Agreements
class EmploymentAgreements(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="employment_agreements"
    )
    types_of_employment_agreements = CustomMarkdownxField(
        help_text="Detail the various types of employment agreements in [Country]. Integrate relevant legal sources within the text to provide accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    essential_clauses = CustomMarkdownxField(
        help_text="Examine the essential clauses that should be included in employment agreements in [Country]. Embed authoritative references to support the discussion. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    probationary_period = CustomMarkdownxField(
        help_text="Explore the concept of the probationary period in employment agreements in [Country]. Incorporate credible sources directly into the guide for validation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    confidentiality_and_non_compete_clauses = CustomMarkdownxField(
        help_text="Discuss the confidentiality and non-compete clauses in employment agreements in [Country]. Seamlessly integrate relevant legal sources within the text. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "F. Employment Agreements"
        verbose_name_plural = "F. Employment Agreements"
        ordering = ["country"]


# 7. Remote work and flexible work arrangements
class RemoteWorkandFlexibleWorkArrangements(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="remote_work"
    )
    remote_work = CustomMarkdownxField(
        help_text="Provide an in-depth analysis of remote work policies and practices in [Country], covering legal regulations, technological infrastructure requirements, and employer responsibilities. Integrate relevant laws and guidelines within the text to ensure accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    flexible_work_arrangements = CustomMarkdownxField(
        help_text="Examine flexible work arrangements in [Country], including part-time work, flexitime, job sharing, and telecommutinP Detail the equipment and expense reimbursements policies, embedding applicable legal sources for verification. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    data_protection_and_privacy = CustomMarkdownxField(
        help_text="Discuss data protection and privacy considerations for remote employees in [Country], highlighting employer obligations, employee rights, and best practices for securing personal and company data. Incorporate authoritative references to support the discussion. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "G. Remote and Flexible Work"
        verbose_name_plural = "G. Remote and Flexible Work"
        ordering = ["country"]


# 8. Standard working hours and overtime


class StandardWorkingHoursandOvertime(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="standard_working_hours"
    )
    standard_working_hours = CustomMarkdownxField(
        help_text="Outline the regulations governing standard working hours in [Country]. Integrate applicable legal references within the content to provide authoritative support. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    overtime = CustomMarkdownxField(
        help_text="Detail the rules and compensation for overtime work in [Country]. Embed relevant legislation and guidelines to ensure accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    rest_periods_and_breaks = CustomMarkdownxField(
        help_text="Examine the entitlements to rest periods and breaks for workers in [Country]. Incorporate authoritative sources directly into the guide for verification. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    night_shift_and_weekend_regulations = CustomMarkdownxField(
        help_text="Discuss the specific regulations for night shift and weekend work in [Country]. Seamlessly integrate applicable legal references within the text. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "H. Working Hours and Overtime"
        verbose_name_plural = "H. Working Hours and Overtime"
        ordering = ["country"]


# 9. Salary and Compensation


class SalaryandCompensation(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="salary_and_compensation"
    )
    market_competitive_salaries = CustomMarkdownxField(
        help_text="Analyze the concept of market competitive salaries in [Country]. Integrate authoritative financial and employment resources within the content for substantiation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    minimum_wage = CustomMarkdownxField(
        help_text="Detail the minimum wage regulations in [Country]. Embed relevant legislative references to ensure accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    bonuses_and_allowances = CustomMarkdownxField(
        help_text="Explore the variety of bonuses and allowances offered to employees in [Country]. Incorporate credible sources directly into the guide for validation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    payroll_cycle = CustomMarkdownxField(
        help_text="Examine the payroll cycle practices in [Country]. Seamlessly integrate authoritative financial and legal references within the text. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "I. Salary and Compensation"
        verbose_name_plural = "I. Salary and Compensation"
        ordering = ["country"]


# 10. Vacation and Leave Policies
class VacationandLeavePolicies(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="vacation_and_leave"
    )
    holiday_leave = CustomMarkdownxField(
        help_text="Detail the vacation leave entitlements in [Country]. Integrate relevant labor laws and guidelines within the text to lend authority. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    public_holidays = CustomMarkdownxField(
        help_text="Explore the public holidays observed in [Country]. Embed authoritative sources to validate the information. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    types_of_leave = CustomMarkdownxField(
        help_text="Examine the various types of leave available to employees in [Country]. Incorporate credible legal and regulatory references directly into the guide for substantiation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "J .Vacation and Leave"
        verbose_name_plural = "J. Vacation and Leave"
        ordering = ["country"]


# 11. Termination and Severance


class Termination(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="termination"
    )
    notice_period = CustomMarkdownxField(
        help_text="Explain the legal requirements for notice periods in [Country] during employment termination. Embed relevant labor law references within the text for credibility. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    severance_pay = CustomMarkdownxField(
        help_text="Detail the severance pay entitlements in [Country]. Incorporate authoritative legal sources to substantiate the information presented. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    termination_process = CustomMarkdownxField(
        help_text="Describe the termination process of employees in [Country]. Seamlessly integrate applicable legal guidelines within the text for validation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "K. Termination and Severance"
        verbose_name_plural = "K. Termination and Severance"
        ordering = ["country"]


# 12. Freelancing and Independent Contracting


class FreelancingandIndependentContracting(models.Model):
    country = models.OneToOneField(
        "Country",
        on_delete=models.PROTECT,
        related_name="freelancing_and_independent_contracting",
    )
    difference_employees_and_contractors = CustomMarkdownxField(
        help_text="Detail the legal distinctions between employees and independent contractors in [Country]. Integrate relevant legal references within the text to ensure accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    independent_contracting = CustomMarkdownxField(
        help_text="Explore the nuances of independent contracting in [Country], including contract structures, negotiation practices, and common industries. Embed authoritative sources to substantiate the discussion. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    intellectual_property_rights = CustomMarkdownxField(
        help_text="Examine intellectual property rights considerations for freelancers and independent contractors in [Country]. Incorporate credible legal sources directly into the text for validation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    tax_and_insurance = CustomMarkdownxField(
        help_text="Describe the tax obligations and insurance options for freelancers and independent contractors in [Country]. Seamlessly integrate relevant tax legislation and insurance norms within the guide. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "L. Independent Contracting"
        verbose_name_plural = "L. Independent Contracting"
        ordering = ["country"]


# 13. Health and Safety Requirements
class HealthandSafetyRequirements(models.Model):
    country = models.OneToOneField(
        "Country",
        on_delete=models.PROTECT,
        related_name="health_and_safety_requirements",
    )
    health_and_safety_laws = CustomMarkdownxField(
        help_text="Provide an in-depth overview of health and safety laws in [Country]. Embed relevant legal references within the text for accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    occupational_health_and_safety = CustomMarkdownxField(
        help_text="Detail the standards and practices for occupational health and safety in [Country].. Incorporate authoritative sources directly into the content for substantiation. UReturn in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    workplace_inspection = CustomMarkdownxField(
        help_text="Examine the role and procedures for workplace inspections in [Country], highlighting inspection criteria, frequency, and follow-up actions. Seamlessly integrate relevant regulations and guidelines within the guide. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    workplace_accidents = CustomMarkdownxField(
        help_text="Discuss the protocols for dealing with workplace accidents in [Country], including reporting requirements, investigation processes, and compensation claims. Embed credible legal and regulatory references to support the discussion. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "M. Health and Safety"
        verbose_name_plural = "M. Health and Safety"
        ordering = ["country"]


# 14. Dispute Resolution and Legal Compliance
class DisputeResolutionandLegalCompliance(models.Model):
    country = models.OneToOneField(
        "Country",
        on_delete=models.PROTECT,
        related_name="dispute_resolution_and_legal_compliance",
    )
    labor_courts_and_arbitration_panels = CustomMarkdownxField(
        help_text="Examine the structure and function of labor courts and arbitration panels in [Country], including their jurisdiction, process, and typical cases handled. Integrate relevant legal sources to provide a comprehensive overview. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    compliance_audits_and_inspections = CustomMarkdownxField(
        help_text="Detail the procedures and importance of compliance audits and inspections in [Country], covering who conducts them, frequency, and the consequences of non-compliance. Embed authoritative references within the text to ensure accuracy. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    reporting_and_whistleblower_protections = CustomMarkdownxField(
        help_text="Discuss the mechanisms for reporting violations and the protections in place for whistleblowers in [Country], highlighting legal provisions and practical considerations. Incorporate credible legal and regulatory references directly into the guide for substantiation. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    international_labor_standards_compliance = CustomMarkdownxField(
        help_text="Explore how [Country] complies with international labor standards, including adherence to conventions and treaties, and the impact on domestic labor laws. Seamlessly integrate relevant international and local legal sources within the text. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "N. Dispute Resolution and Legal"
        verbose_name_plural = "N. Dispute Resolution and Legal"
        ordering = ["country"]


# 15. Cultural Considerations


class CulturalConsiderations(models.Model):
    country = models.OneToOneField(
        "Country", on_delete=models.PROTECT, related_name="cultural_considerations"
    )
    communication_styles_in_the_workplace = CustomMarkdownxField(
        help_text="Detail the prevalent communication styles in the workplace in [Country], including directness, formality, and the role of non-verbal cues. Embed relevant cultural studies and business practices within the text to offer depth. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    negotiation_practices = CustomMarkdownxField(
        help_text="Examine negotiation practices in [Country], focusing on approaches, typical strategies, and cultural norms that influence business dealings. Integrate authoritative references to enhance credibility. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    understanding_hierarchical_structures = CustomMarkdownxField(
        help_text="Explore the hierarchical structures prevalent in businesses in [Country], including the impact on decision-making, team dynamics, and leadership styles. Incorporate insights from cultural analysis and management theories directly into the content. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )
    holidays_and_observances_affecting_business_operations = CustomMarkdownxField(
        help_text="Describe the major holidays and observances in [Country] that affect business operations, including statutory holidays, regional observances, and their impact on work schedules. Seamlessly embed cultural and legal references within the text. Return in markdown, start with H2 headings and use H3, H4 if needed. Only return the guide and do not add disclaimers. Don't add invalid URL's"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "O. Cultural Considerations"
        verbose_name_plural = "O. Cultural Considerations"
        ordering = ["country"]
