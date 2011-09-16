"""
    Copyright 2011 Martin Paul EVe

    This file is part of Vheissu.

    Vheissu is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    Vheissu is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Vheissu. If not, see http://www.gnu.org/licenses/.
"""


from django.db import models

class author(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    
class venue(models.Model):
    venue_name = models.CharField(max_length=60)
    
class ptype(models.Model):
    type = models.CharField(max_length=30)

class pdate(models.Model):
    date = models.DateField()
    
class publisher(models.Model):
    publisher_name = models.CharField(max_length=60)
    
class publication_place(models.Model):
    place = models.CharField(max_length=60)  
    
class document(models.Model):
    doc_document_name = models.CharField(max_length=255)
    doc_pages = models.CharField(max_length=255, null=True)
    doc_venue = models.ForeignKey(venue, null=True)
    doc_authors = models.ManyToManyField(author, through='document_author')
    doc_type = models.ManyToManyField(ptype, through='document_type')
    doc_publisher = models.ManyToManyField(publisher, through='document_publisher')
    doc_publication = models.ManyToManyField(publication_place, through='document_publication_place')
    doc_date = models.ManyToManyField(pdate, through='document_date')
    doc_issue = models.CharField(max_length=255, null=True)
    doc_notes = models.CharField(max_length=255, null=True)
    
class document_author(models.Model):
    author = models.ForeignKey(author)
    document = models.ForeignKey(document)
    
class document_type(models.Model):
    dtype = models.ForeignKey(ptype)
    document = models.ForeignKey(document)
    
class document_publisher(models.Model):
    publisher = models.ForeignKey(publisher)
    document = models.ForeignKey(document)
    
class document_publication_place(models.Model):
    publication_place = models.ForeignKey(publication_place)
    document = models.ForeignKey(document)
    
class document_date(models.Model):
    date = models.ForeignKey(pdate)
    document = models.ForeignKey(document)
