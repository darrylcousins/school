__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.db import models


class Activities(models.Model):
    activityid = models.AutoField(
        db_column='ActivityId', 
        primary_key=True)
    name = models.CharField(db_column='Name', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Activities'
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'



class Appinfo(models.Model):
    property = models.CharField(db_column='Property', max_length=255)
    value = models.CharField(db_column='Value', max_length=255)

    class Meta:
        managed = False
        db_table = 'AppInfo'


class ApplianceProperties(models.Model):
    appliancepropertyid = models.AutoField(
        db_column='AppliancePropertyId',
        primary_key=True)
    applianceid = models.ForeignKey(
        'Appliances',
        models.DO_NOTHING,
        db_column='ApplianceId')
    name = models.CharField(db_column='Name', max_length=20)
    value = models.CharField(
        db_column='Value',
        max_length=50,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'ApplianceProperties'
        verbose_name = 'Appliance Property'
        verbose_name_plural = 'Appliance Properties'


class Appliances(models.Model):
    applianceid = models.AutoField(db_column='ApplianceId', primary_key=True)
    appliancetag = models.CharField(db_column='ApplianceTag', max_length=25)
    testdate = models.DateTimeField(
        db_column='TestDate', blank=True, null=True)
    retestdate = models.DateTimeField(
        db_column='RetestDate', blank=True, null=True)
    location = models.CharField(
        db_column='Location',
        max_length=20,
        blank=True,
        null=True)
    userid = models.ForeignKey(
        'Users',
        models.DO_NOTHING,
        db_column='UserId',
        blank=True,
        null=True)
    comment = models.TextField(db_column='Comment', blank=True, null=True)
    activityid = models.ForeignKey(
        Activities,
        models.DO_NOTHING,
        db_column='ActivityId',
        blank=True,
        null=True)
    status = models.SmallIntegerField(
        db_column='Status', blank=True, null=True)
    premisesid = models.ForeignKey(
        'Premises',
        models.DO_NOTHING,
        db_column='PremisesId')
    nextapplianceid = models.IntegerField(
        db_column='NextApplianceId', blank=True, null=True)
    patid = models.ForeignKey(
        'Pats',
        models.DO_NOTHING,
        db_column='PATId',
        blank=True,
        null=True)
    archived = models.SmallIntegerField(
        db_column='Archived', blank=True, null=True)
    appliancename = models.CharField(
        db_column='ApplianceName',
        max_length=50,
        blank=True,
        null=True)
    appliance2tag = models.CharField(
        db_column='Appliance2Tag',
        max_length=25,
        blank=True,
        null=True)
    appliance2name = models.CharField(
        db_column='Appliance2Name',
        max_length=50,
        blank=True,
        null=True)
    repaircodeid = models.ForeignKey(
        'RepairCodes',
        models.DO_NOTHING,
        db_column='RepairCodeId',
        blank=True,
        null=True)
    site = models.CharField(
        db_column='Site',
        max_length=50,
        blank=True,
        null=True)
    patid2 = models.IntegerField(db_column='PATId2', blank=True, null=True)
    attachments = models.TextField(
        db_column='Attachments', blank=True, null=True)

    def __str__(self):
        return self.appliancename

    class Meta:
        managed = False
        db_table = 'Appliances'
        verbose_name = 'Appliance'
        verbose_name_plural = 'Appliances'


class AutoTestGroups(models.Model):
    autotestgroupid = models.AutoField(db_column='AutoTestGroupId', primary_key=True)
    name = models.CharField(db_column='Name', max_length=20)
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=10)
    grouptype = models.SmallIntegerField(db_column='GroupType')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'AutoTestGroups'


class AutoTests(models.Model):
    autotestid = models.AutoField(db_column='AutoTestId', primary_key=True)
    testcode = models.CharField(db_column='TestCode', max_length=255)
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=20)
    name = models.CharField(
        db_column='Name',
        max_length=20,
        blank=True,
        null=True)
    autotestgroupid = models.ForeignKey(
        AutoTestGroups,
        models.DO_NOTHING,
        db_column='AutoTestGroupId',
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'AutoTests'
        verbose_name = 'Auto Test'
        verbose_name_plural = 'Auto Tests'


class BusinessSubjects(models.Model):
    subjectid = models.AutoField(db_column='SubjectId', primary_key=True)
    nametype = models.IntegerField(db_column='NameType')
    name = models.CharField(
        db_column='Name',
        max_length=50,
        blank=True,
        null=True)
    description = models.CharField(
        db_column='Description',
        max_length=512,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'BusinessSubjects'
        verbose_name = 'Business Subject'
        verbose_name_plural = 'Business Subjects'


class Checkbox(models.Model):
    checkboxid = models.AutoField(db_column='CheckBoxId', primary_key=True)
    datalistitemid = models.ForeignKey(
        'DataListItems',
        models.DO_NOTHING,
        db_column='DataListItemId')
    functionname = models.CharField(db_column='FunctionName', max_length=30)
    ref = models.CharField(db_column='Ref', max_length=20)
    upperlimit = models.CharField(
        db_column='UpperLimit',
        max_length=18,
        blank=True,
        null=True)
    lowerlimit = models.CharField(
        db_column='LowerLimit',
        max_length=18,
        blank=True,
        null=True)
    result = models.CharField(
        db_column='Result',
        max_length=18,
        blank=True,
        null=True)
    status = models.SmallIntegerField(
        db_column='Status', blank=True, null=True)
    functionindex = models.IntegerField(
        db_column='FunctionIndex', blank=True, null=True)
    functiongroup = models.CharField(
        db_column='FunctionGroup',
        max_length=30,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'CheckBox'


class Customers(models.Model):
    customerid = models.AutoField(db_column='CustomerId', primary_key=True)
    name = models.CharField(db_column='Name', max_length=50)
    department = models.CharField(
        db_column='Department',
        max_length=20,
        blank=True,
        null=True)
    contact = models.CharField(
        db_column='Contact',
        max_length=20,
        blank=True,
        null=True)
    street1 = models.CharField(
        db_column='Street1',
        max_length=50,
        blank=True,
        null=True)
    street2 = models.CharField(
        db_column='Street2',
        max_length=50,
        blank=True,
        null=True)
    city = models.CharField(
        db_column='City',
        max_length=20,
        blank=True,
        null=True)
    country = models.CharField(
        db_column='Country',
        max_length=20,
        blank=True,
        null=True)
    phone = models.CharField(
        db_column='Phone',
        max_length=20,
        blank=True,
        null=True)
    fax = models.CharField(
        db_column='Fax',
        max_length=20,
        blank=True,
        null=True)
    url = models.CharField(
        db_column='Url',
        max_length=50,
        blank=True,
        null=True)
    email = models.CharField(
        db_column='Email',
        max_length=50,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Customers'


class DataListGroups(models.Model):
    datalistgroupid = models.AutoField(db_column='DataListGroupId', primary_key=True)
    datalisttypeid = models.ForeignKey(
        'DataListTypes',
        models.DO_NOTHING,
        db_column='DataListTypeId')
    name = models.CharField(db_column='Name', max_length=40)
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'DataListGroups'


class DataListItems(models.Model):
    datalistitemid = models.AutoField(db_column='DataListItemId', primary_key=True)
    datalistgroupid = models.ForeignKey(
        DataListGroups,
        models.DO_NOTHING,
        db_column='DataListGroupId')
    value = models.CharField(
        db_column='Value',
        max_length=255,
        blank=True,
        null=True)
    name = models.CharField(db_column='Name', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'DataListItems'


class DataListTypes(models.Model):
    datalisttypeid = models.AutoField(db_column='DataListTypeId', primary_key=True)
    name = models.CharField(db_column='Name', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'DataListTypes'


class FunctionTypes(models.Model):
    functiontypeid = models.AutoField(db_column='FunctionTypeId', primary_key=True)
    name = models.CharField(db_column='Name', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'FunctionTypes'


class Functions(models.Model):
    functionid = models.AutoField(db_column='FunctionId', primary_key=True)
    applianceid = models.ForeignKey(
        Appliances,
        models.DO_NOTHING,
        db_column='ApplianceId')
    functiontypeid = models.ForeignKey(
        FunctionTypes,
        models.DO_NOTHING,
        db_column='FunctionTypeId')
    autotestid = models.ForeignKey(
        AutoTests,
        models.DO_NOTHING,
        db_column='AutoTestId',
        blank=True,
        null=True)
    status = models.SmallIntegerField(db_column='Status')

    class Meta:
        managed = False
        db_table = 'Functions'
        verbose_name = 'Function'
        verbose_name_plural = 'Functions'


class Limits(models.Model):
    limitid = models.AutoField(db_column='LimitId', primary_key=True)
    functionid = models.ForeignKey(
        Functions,
        models.DO_NOTHING,
        db_column='FunctionId')
    name = models.CharField(db_column='Name', max_length=30)
    value1 = models.CharField(
        db_column='Value1',
        max_length=25,
        blank=True,
        null=True)
    value2 = models.CharField(
        db_column='Value2',
        max_length=20,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Limits'


class Pats(models.Model):
    patid = models.AutoField(db_column='PATId', primary_key=True)
    name = models.CharField(
        db_column='Name',
        max_length=30,
        blank=True,
        null=True)
    mi = models.CharField(db_column='MI', max_length=20, blank=True, null=True)
    swversion = models.CharField(
        db_column='SWVersion',
        max_length=20,
        blank=True,
        null=True)
    serialnumber = models.CharField(db_column='SerialNumber', max_length=20)
    lastcalibration = models.DateTimeField(
        db_column='LastCalibration', blank=True, null=True)
    type = models.CharField(
        db_column='Type',
        max_length=10,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'PATS'


class Parameters(models.Model):
    parameterid = models.AutoField(db_column='ParameterId', primary_key=True)
    functionid = models.ForeignKey(
        Functions,
        models.DO_NOTHING,
        db_column='FunctionId')
    name = models.CharField(db_column='Name', max_length=30)
    value = models.CharField(
        db_column='Value',
        max_length=20,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Parameters'


class Premises(models.Model):
    premisesid = models.AutoField(db_column='PremisesId', primary_key=True)
    name = models.CharField(db_column='Name', max_length=50)
    projectid = models.ForeignKey(
        'Projects',
        models.DO_NOTHING,
        db_column='ProjectId')
    nextpremisesid = models.IntegerField(
        db_column='NextPremisesId', blank=True, null=True)
    parentid = models.ForeignKey(
        'self',
        models.DO_NOTHING,
        db_column='ParentId',
        blank=True,
        null=True)
    archived = models.SmallIntegerField(
        db_column='Archived', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Premises'
        verbose_name = 'Premise'
        verbose_name_plural = 'Premises'


class Projects(models.Model):
    projectid = models.AutoField(db_column='ProjectId', primary_key=True)
    name = models.CharField(db_column='Name', max_length=20)
    validatorid = models.ForeignKey(
        BusinessSubjects,
        models.DO_NOTHING,
        db_column='ValidatorId',
        related_name="metrel_validator_projects_related",
        blank=True,
        null=True)
    customerid = models.ForeignKey(
        BusinessSubjects,
        models.DO_NOTHING,
        db_column='CustomerId',
        related_name="metrel_customer_projects_related",
        blank=True,
        null=True)
    archived = models.SmallIntegerField(
        db_column='Archived', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class RepairCodes(models.Model):
    repaircodeid = models.AutoField(db_column='RepairCodeId', primary_key=True)
    repaircode = models.CharField(db_column='RepairCode', max_length=20)
    description = models.CharField(
        db_column='Description',
        max_length=100,
        blank=True,
        null=True)
    price = models.FloatField(db_column='Price', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RepairCodes'


class Results(models.Model):
    resultid = models.AutoField(db_column='ResultId', primary_key=True)
    limitid = models.ForeignKey(Limits, models.DO_NOTHING, db_column='LimitId')
    status = models.SmallIntegerField(db_column='Status')
    value = models.CharField(
        db_column='Value',
        max_length=20,
        blank=True,
        null=True)
    quantity = models.CharField(
        db_column='Quantity',
        max_length=15,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Results'
        verbose_name = 'Results'
        verbose_name_plural = 'Results'


class Translations(models.Model):
    translationid = models.AutoField(db_column='TranslationId', primary_key=True)
    name = models.CharField(db_column='Name', max_length=30)
    culture = models.CharField(db_column='Culture', max_length=50)
    translation = models.CharField(db_column='Translation', max_length=50)
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=50)

    class Meta:
        managed = False
        db_table = 'Translations'


class Users(models.Model):
    userid = models.AutoField(db_column='UserId', primary_key=True)
    firstname = models.CharField(db_column='FirstName', max_length=20)
    lastname = models.CharField(
        db_column='LastName',
        max_length=20,
        blank=True,
        null=True)
    department = models.CharField(
        db_column='Department',
        max_length=50,
        blank=True,
        null=True)
    phone = models.CharField(
        db_column='Phone',
        max_length=20,
        blank=True,
        null=True)
    fax = models.CharField(
        db_column='Fax',
        max_length=20,
        blank=True,
        null=True)
    email = models.CharField(
        db_column='Email',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Users'


class Validators(models.Model):
    validatorid = models.AutoField(db_column='ValidatorId', primary_key=True)
    firstname = models.CharField(db_column='FirstName', max_length=20)
    lastname = models.CharField(db_column='LastName', max_length=20)
    company = models.CharField(
        db_column='Company',
        max_length=20,
        blank=True,
        null=True)
    department = models.CharField(
        db_column='Department',
        max_length=20,
        blank=True,
        null=True)
    phone = models.CharField(
        db_column='Phone',
        max_length=20,
        blank=True,
        null=True)
    fax = models.CharField(
        db_column='Fax',
        max_length=20,
        blank=True,
        null=True)
    email = models.CharField(
        db_column='Email',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Validators'


class SysDiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
