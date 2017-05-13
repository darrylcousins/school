# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from __future__ import unicode_literals

from django.db import models


class Activities(models.Model):
    activityid = models.AutoField(db_column='ActivityId')
    name = models.CharField(db_column='Name', max_length=50)

    class Meta:
        managed = False
        db_table = 'Activities'


class Appinfo(models.Model):
    property = models.CharField(db_column='Property', max_length=255)
    value = models.CharField(db_column='Value', max_length=255)

    class Meta:
        managed = False
        db_table = 'AppInfo'


class Applianceproperties(models.Model):
    appliancepropertyid = models.AutoField(db_column='AppliancePropertyId')
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

    class Meta:
        managed = False
        db_table = 'ApplianceProperties'


class Appliances(models.Model):
    applianceid = models.AutoField(db_column='ApplianceId')
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
        null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)
    activityid = models.ForeignKey(
        Activities,
        models.DO_NOTHING,
        db_column='ActivityId',
        blank=True,
        null=True)  # Field name made lowercase.
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
        null=True)  # Field name made lowercase.
    appliance2tag = models.CharField(
        db_column='Appliance2Tag',
        max_length=25,
        blank=True,
        null=True)  # Field name made lowercase.
    appliance2name = models.CharField(
        db_column='Appliance2Name',
        max_length=50,
        blank=True,
        null=True)  # Field name made lowercase.
    repaircodeid = models.ForeignKey(
        'Repaircodes',
        models.DO_NOTHING,
        db_column='RepairCodeId',
        blank=True,
        null=True)  # Field name made lowercase.
    site = models.CharField(
        db_column='Site',
        max_length=50,
        blank=True,
        null=True)
    patid2 = models.IntegerField(db_column='PATId2', blank=True, null=True)
    attachments = models.TextField(
        db_column='Attachments', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Appliances'


class Autotestgroups(models.Model):
    autotestgroupid = models.AutoField(db_column='AutoTestGroupId')
    name = models.CharField(db_column='Name', max_length=20)
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=10)
    grouptype = models.SmallIntegerField(db_column='GroupType')

    class Meta:
        managed = False
        db_table = 'AutoTestGroups'


class Autotests(models.Model):
    autotestid = models.AutoField(db_column='AutoTestId')
    testcode = models.CharField(db_column='TestCode', max_length=255)
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=20)
    name = models.CharField(
        db_column='Name',
        max_length=20,
        blank=True,
        null=True)
    autotestgroupid = models.ForeignKey(
        Autotestgroups,
        models.DO_NOTHING,
        db_column='AutoTestGroupId',
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AutoTests'


class Businesssubjects(models.Model):
    # Field name made lowercase.
    subjectid = models.AutoField(db_column='SubjectId')
    # Field name made lowercase.
    nametype = models.IntegerField(db_column='NameType')
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name',
        max_length=50,
        blank=True,
        null=True)
    description = models.CharField(
        db_column='Description',
        max_length=512,
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BusinessSubjects'


class Checkbox(models.Model):
    # Field name made lowercase.
    checkboxid = models.AutoField(db_column='CheckBoxId')
    datalistitemid = models.ForeignKey(
        'Datalistitems',
        models.DO_NOTHING,
        db_column='DataListItemId')  # Field name made lowercase.
    # Field name made lowercase.
    functionname = models.CharField(db_column='FunctionName', max_length=30)
    # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=20)
    # Field name made lowercase.
    upperlimit = models.CharField(
        db_column='UpperLimit',
        max_length=18,
        blank=True,
        null=True)
    # Field name made lowercase.
    lowerlimit = models.CharField(
        db_column='LowerLimit',
        max_length=18,
        blank=True,
        null=True)
    # Field name made lowercase.
    result = models.CharField(
        db_column='Result',
        max_length=18,
        blank=True,
        null=True)
    # Field name made lowercase.
    status = models.SmallIntegerField(
        db_column='Status', blank=True, null=True)
    # Field name made lowercase.
    functionindex = models.IntegerField(
        db_column='FunctionIndex', blank=True, null=True)
    functiongroup = models.CharField(
        db_column='FunctionGroup',
        max_length=30,
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CheckBox'


class Customers(models.Model):
    # Field name made lowercase.
    customerid = models.AutoField(db_column='CustomerId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)
    # Field name made lowercase.
    department = models.CharField(
        db_column='Department',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    contact = models.CharField(
        db_column='Contact',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    street1 = models.CharField(
        db_column='Street1',
        max_length=50,
        blank=True,
        null=True)
    # Field name made lowercase.
    street2 = models.CharField(
        db_column='Street2',
        max_length=50,
        blank=True,
        null=True)
    # Field name made lowercase.
    city = models.CharField(
        db_column='City',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    country = models.CharField(
        db_column='Country',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    phone = models.CharField(
        db_column='Phone',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    fax = models.CharField(
        db_column='Fax',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    url = models.CharField(
        db_column='Url',
        max_length=50,
        blank=True,
        null=True)
    # Field name made lowercase.
    email = models.CharField(
        db_column='Email',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Customers'


class Datalistgroups(models.Model):
    # Field name made lowercase.
    datalistgroupid = models.AutoField(db_column='DataListGroupId')
    datalisttypeid = models.ForeignKey(
        'Datalisttypes',
        models.DO_NOTHING,
        db_column='DataListTypeId')  # Field name made lowercase.
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40)
    # Field name made lowercase.
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=40)

    class Meta:
        managed = False
        db_table = 'DataListGroups'


class Datalistitems(models.Model):
    # Field name made lowercase.
    datalistitemid = models.AutoField(db_column='DataListItemId')
    datalistgroupid = models.ForeignKey(
        Datalistgroups,
        models.DO_NOTHING,
        db_column='DataListGroupId')  # Field name made lowercase.
    # Field name made lowercase.
    value = models.CharField(
        db_column='Value',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20)

    class Meta:
        managed = False
        db_table = 'DataListItems'


class Datalisttypes(models.Model):
    # Field name made lowercase.
    datalisttypeid = models.AutoField(db_column='DataListTypeId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20)

    class Meta:
        managed = False
        db_table = 'DataListTypes'


class Functiontypes(models.Model):
    # Field name made lowercase.
    functiontypeid = models.AutoField(db_column='FunctionTypeId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)

    class Meta:
        managed = False
        db_table = 'FunctionTypes'


class Functions(models.Model):
    # Field name made lowercase.
    functionid = models.AutoField(db_column='FunctionId')
    # Field name made lowercase.
    applianceid = models.ForeignKey(
        Appliances,
        models.DO_NOTHING,
        db_column='ApplianceId')
    # Field name made lowercase.
    functiontypeid = models.ForeignKey(
        Functiontypes,
        models.DO_NOTHING,
        db_column='FunctionTypeId')
    autotestid = models.ForeignKey(
        Autotests,
        models.DO_NOTHING,
        db_column='AutoTestId',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')

    class Meta:
        managed = False
        db_table = 'Functions'


class Limits(models.Model):
    # Field name made lowercase.
    limitid = models.AutoField(db_column='LimitId')
    # Field name made lowercase.
    functionid = models.ForeignKey(
        Functions,
        models.DO_NOTHING,
        db_column='FunctionId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)
    # Field name made lowercase.
    value1 = models.CharField(
        db_column='Value1',
        max_length=25,
        blank=True,
        null=True)
    # Field name made lowercase.
    value2 = models.CharField(
        db_column='Value2',
        max_length=20,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Limits'


class Pats(models.Model):
    patid = models.AutoField(db_column='PATId')  # Field name made lowercase.
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name',
        max_length=30,
        blank=True,
        null=True)
    # Field name made lowercase.
    mi = models.CharField(db_column='MI', max_length=20, blank=True, null=True)
    # Field name made lowercase.
    swversion = models.CharField(
        db_column='SWVersion',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber', max_length=20)
    # Field name made lowercase.
    lastcalibration = models.DateTimeField(
        db_column='LastCalibration', blank=True, null=True)
    # Field name made lowercase.
    type = models.CharField(
        db_column='Type',
        max_length=10,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'PATS'


class Parameters(models.Model):
    # Field name made lowercase.
    parameterid = models.AutoField(db_column='ParameterId')
    # Field name made lowercase.
    functionid = models.ForeignKey(
        Functions,
        models.DO_NOTHING,
        db_column='FunctionId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)
    # Field name made lowercase.
    value = models.CharField(
        db_column='Value',
        max_length=20,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Parameters'


class Premises(models.Model):
    # Field name made lowercase.
    premisesid = models.AutoField(db_column='PremisesId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)
    # Field name made lowercase.
    projectid = models.ForeignKey(
        'Projects',
        models.DO_NOTHING,
        db_column='ProjectId')
    # Field name made lowercase.
    nextpremisesid = models.IntegerField(
        db_column='NextPremisesId', blank=True, null=True)
    parentid = models.ForeignKey(
        'self',
        models.DO_NOTHING,
        db_column='ParentId',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    archived = models.SmallIntegerField(
        db_column='Archived', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Premises'


class Projects(models.Model):
    # Field name made lowercase.
    projectid = models.AutoField(db_column='ProjectId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20)
    validatorid = models.ForeignKey(
        Businesssubjects,
        models.DO_NOTHING,
        db_column='ValidatorId',
        blank=True,
        null=True)  # Field name made lowercase.
    customerid = models.ForeignKey(
        Businesssubjects,
        models.DO_NOTHING,
        db_column='CustomerId',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    archived = models.SmallIntegerField(
        db_column='Archived', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Projects'


class Repaircodes(models.Model):
    # Field name made lowercase.
    repaircodeid = models.AutoField(db_column='RepairCodeId')
    # Field name made lowercase.
    repaircode = models.CharField(db_column='RepairCode', max_length=20)
    description = models.CharField(
        db_column='Description',
        max_length=100,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RepairCodes'


class Results(models.Model):
    # Field name made lowercase.
    resultid = models.AutoField(db_column='ResultId')
    # Field name made lowercase.
    limitid = models.ForeignKey(Limits, models.DO_NOTHING, db_column='LimitId')
    # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')
    # Field name made lowercase.
    value = models.CharField(
        db_column='Value',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    quantity = models.CharField(
        db_column='Quantity',
        max_length=15,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Results'


class Translations(models.Model):
    # Field name made lowercase.
    translationid = models.AutoField(db_column='TranslationId')
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)
    # Field name made lowercase.
    culture = models.CharField(db_column='Culture', max_length=50)
    # Field name made lowercase.
    translation = models.CharField(db_column='Translation', max_length=50)
    # Field name made lowercase.
    instrumentname = models.CharField(
        db_column='InstrumentName', max_length=50)

    class Meta:
        managed = False
        db_table = 'Translations'


class Users(models.Model):
    userid = models.AutoField(db_column='UserId')  # Field name made lowercase.
    # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=20)
    # Field name made lowercase.
    lastname = models.CharField(
        db_column='LastName',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    department = models.CharField(
        db_column='Department',
        max_length=50,
        blank=True,
        null=True)
    # Field name made lowercase.
    phone = models.CharField(
        db_column='Phone',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    fax = models.CharField(
        db_column='Fax',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    email = models.CharField(
        db_column='Email',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Users'


class Validators(models.Model):
    # Field name made lowercase.
    validatorid = models.AutoField(db_column='ValidatorId')
    # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=20)
    # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=20)
    # Field name made lowercase.
    company = models.CharField(
        db_column='Company',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    department = models.CharField(
        db_column='Department',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    phone = models.CharField(
        db_column='Phone',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    fax = models.CharField(
        db_column='Fax',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    email = models.CharField(
        db_column='Email',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'Validators'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
