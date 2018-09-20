# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random
import sys

import names

from django.core.wsgi import get_wsgi_application
from django.core.files import File


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waldur_core.server.settings')

get_wsgi_application()

from waldur_mastermind.marketplace.models import Category, Section, Attribute, AttributeOption, Offering, ServiceProvider
from waldur_core.structure.models import Customer


# attribute types
boolean = 'boolean'
string = 'string'
integer = 'integer'
choice = 'choice'
listattr = 'list'

# Location where images are located
base = '/Users/ilja/workspace/estcloud/marketplace-schema/'  # path relative to the cwd or absolute

categories = [
    ('Compute', 'Computing services', 'server.svg'),
    ('Storage', 'Data preservation', 'database.svg'),
    ('Backup', 'Backup solutions', 'data.svg'),
    ('Security', 'X-road, antivirus etc', 'shield.svg'),
    ('CMS', 'Contnent Management System', 'sharing-content.svg'),
    ('Operations', 'Experts in support', 'support.svg'),
]

common_sections = {
    'Support': [
        ('email', 'E-mail', string),
        ('phone', 'Phone', string),
        ('portal', 'Support portal', string),
        ('guide', 'User guide', string),
    ],
    'Security': [
        ('certification', 'Certification', listattr),
    ],
}

compute_sections = {
    'Virtualization': [
        ('virtualization', 'Virtualization', choice),
    ],
}

storage_sections = {
    'Encryption': [
        ('encryption_at_rest', 'Encryption at rest', boolean),
    ],
}

operations_sections = {
    'Communication': [
        ('languages', 'Languages', listattr),
    ],
    'SLA': [
        ('workdays', 'Work days', listattr),
        ('businesshours', 'Business hours', listattr),
        ('priority', 'Priority', listattr),
    ]
}

cms_sections = {
    'Deployment': [
        ('deployment_type', 'Deployment type', choice),
    ],
}

extra_sections = {
    'Compute': compute_sections,
    'Storage': storage_sections,
    'Operations': operations_sections,
    'CMS': cms_sections,
}

enums = {
    'languages': [
        ('et', 'Estonian'),
        ('en', 'English'),
        ('lv', 'Latvian'),
        ('lt', 'Lithuanian'),
        ('ru', 'Russian'),
        ('sw', 'Swedish'),
        ('fi', 'Finnish'),
    ],
    'deployment_type': [
        ('appliance', 'Appliance (Managed)'),
        ('remote', 'Remote (SaaS)')
    ],
    'workdays': [
        ('base', '5 days'),
        ('extended', '7 days'),
    ],
    'businesshours': [
        ('basehours', '8 hours'),
        ('extendedhours', '24 hours'),
    ],
    'priority': [
        ('ASAP', 'As soon as possible'),
        ('EOB', 'End-of-business day'),
        ('NBD', 'Next business day'),
    ],
    'certification': [
        ('iskem', 'ISKE M'),
        ('iskeh', 'ISKE H'),
        ('iskel', 'ISKE L'),
        ('iso27001', 'ISO27001'),
        ('vahtiraised', 'VAHTI raised level'),
    ],
    'interconnect': [
        ('Infiniband_FDR', 'Infiniband FDR'),
        ('Infiniband_EDR', 'Infiniband EDR'),
        ('Ethernet_1G', 'Ethernet 1G'),
        ('Ethernet_10G', 'Ethernet 10G'),
    ],
    'virtualization': [
        ('KVM', 'KVM'),
        ('XEN', 'XEN'),
        ('VMware', 'Ethernet 1G'),
        ('Baremetal', 'Baremetal'),
    ],

}

expert_configuration = {
        'prefill_name': True,  # If True, name would be pre-filled with label in request creation form
        'order': ['special'],
        'options': {
            'special': {
                'type': 'string',
                'label': 'Custom desire',
                'help_text': 'Special requests',
                'required': False,  # if field must be provided by a user.
            }
        }
    }


def generate_offerings(category):
    for i in xrange(random.randint(1, 20)):
        customer, _ = Customer.objects.get_or_create(
            name='Organization %s' % i,
            email='support@example.com',
            registration_code='EE123321123',
            vat_code='1231231231',
        )
        nr = random.randint(1, 16)
        customer.image.save('company_%s.jpg' % nr, File(open(base + 'companies/company_%s.jpg' % nr, 'r')))

        ServiceProvider.objects.get_or_create(
            customer=customer,
            enable_notifications=False,
        )
        offering, _ = Offering.objects.get_or_create(
            name=names.get_full_name(),
            category=category,
            state=Offering.States.ACTIVE,
            description='Great expert capable of delivering wonders',
            full_description='<h2>Overview</h2>The life of expert has been long and prosperous. The life of expert has '
                             'been long and prosperous.The life of expert has been long and prosperous. The life of '
                             'expert has been long and prosperous.',
            rating=random.randint(1, 5),
            customer=customer,
            type='Support.OfferingTemplate',
            geolocations=[{"latitude": 55.7119513, "longitude": 13.2013043}],
            attributes={
                u'personal_name': [u'ABC XYZ'],
                u'personal_oneliner': [u'Something great so far'],
                u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
                u'node_information_local_disk': 200,
                u'node_information_memory': 64,
                u'node_information_node_count': 584,
                u'performance_linpak': 462.4,
                u'performance_tflops': 766.6,
                u'software_applications': [u'software_applications_Matlab', u'software_applications_Gromacs'],
                u'system_information_home_space': u'/home/TBA',
                u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
                u'system_information_queing_system': [u'system_information_queing_system_slurm'],
                u'system_information_work_space': u'/tmp',
                u'support_email': u'servicedesk@csc.fi',
                u'support_phone': u'+358 (0) 94 57 2821',
                u'support_portal': u'https://research.csc.fi/support',
            },
            options=expert_configuration,
        )
        #nr = random.randint(1, 5)
        #offering.thumbnail.save('person_%s.jpg' % nr, File(open(base + 'people/person_%s.jpg' % nr, 'r')))


def populate_section(section_key, section_data, cat):
    sec, _ = Section.objects.get_or_create(key="%s_%s" % (cat.title, section_key), title=section_key,
                                           category=cat)
    sec.is_standalone = True
    sec.save()
    for attribute in section_data[section_key]:
        key, title, type = attribute
        attr, _ = Attribute.objects.get_or_create(key='%s_%s_%s' % (cat.title, section_key, key), title=title,
                                                  type=type,
                                                  section=sec)
        if key in enums:
            values = enums[key]
            for val_key, val_label in values:
                AttributeOption.objects.get_or_create(attribute=attr,
                                                      key='%s_%s_%s_%s' % (cat.title, section_key, key, val_key),
                                                      title=val_label)


def populate_attributes(cat):
    # populate common
    for section_key in common_sections.keys():
        populate_section(section_key, common_sections, cat)

    if cat.title in extra_sections.keys():
        for section_key in extra_sections[cat.title].keys():
            populate_section(section_key, extra_sections[cat.title], cat)


for cat in categories:
    title, description, icon_name = cat
    new_category, _ = Category.objects.get_or_create(title=title, description=description)
    new_category.icon.save(icon_name, File(open(base + icon_name, 'r')))
    new_category.save()
    populate_attributes(new_category)
    #generate_offerings(new_category)
