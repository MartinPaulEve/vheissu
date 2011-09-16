"""
    Copyright 2011 Martin Paul EVe

    This file is part of Vheissu.

    Vheissu is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    Vheissu is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Vheissu. If not, see http://www.gnu.org/licenses/.
"""

from django.http import HttpResponse
import datetime
import re
from BeautifulSoup import BeautifulSoup
import models



def run_import(request):
    
    article_regex = '\s*(.+?)\.\s*"\s*<strong>\s*(.+?)\s*</strong>\s*\."\s*<i>\s*(.+?)\s*</i>\s*(.+?)\s*\((\d+?)\):\s*(.+?)\.\s*<i>\s*(.+?)\s*</i>'
    bookchapter_regex = '\s*(.+?)\.\s+ \"<strong>(.+?)</strong>\."\s+<i>(.+?)</i>\s*\.\s*(.+?),\s*(.+?)\((\d+)\)\:\s*(.+?)\.\s*<i>(.+?)</i>'
    html = ''
    
    with open('/home/martin/Documents/Programming/Pynchon_Biblio/new.txt' ,'r') as f:
    #with open('/home/martin/Documents/Programming/Pynchon_Biblio/test2.xml' ,'r') as f:
        soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
    
        slist = soup.findAll(['p'])

        for line in slist:
            cont = True
            
            article_result = re.match(article_regex, line.renderContents())
            
            if article_result:
            
                venue, created = models.venue.objects.get_or_create(venue_name=article_result.group(3).strip())
                    
                article, created = models.document.objects.get_or_create(doc_document_name=article_result.group(2), doc_venue=venue, doc_pages=article_result.group(6).strip(), doc_issue=article_result.group(4).strip(), doc_notes=article_result.group(7).strip())
                
                authors = article_result.group(1).split(' and ')
                for author in authors:
                    if ',' in author:
                        author_split = author.split(',')
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[1].strip(), last_name=author_split[0].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=article)
                    else:
                        author_split = author.rsplit(' ', 1)
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[0].strip(), last_name=author_split[1].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=article)
                
                publication_date, created = models.pdate.objects.get_or_create(date=datetime.datetime.strptime(article_result.group(5).strip(), '%Y'))
                doc_publication_date, created = models.document_date.objects.get_or_create(date=publication_date, document=article)
                
                publication_type, created = models.ptype.objects.get_or_create(type='Article')
                doc_document_type, created = models.document_type.objects.get_or_create(dtype=publication_type, document=article)
        
                line.extract()
                cont = False

            bookchapter_result = re.match(bookchapter_regex, line.renderContents())
    
            if bookchapter_result and cont:
                
                venue, created = models.venue.objects.get_or_create(venue_name=bookchapter_result.group(3).strip())
                
                book_chapter, created = models.document.objects.get_or_create(doc_document_name=bookchapter_result.group(2), doc_venue=venue, doc_pages=bookchapter_result.group(7).strip())
                
                authors = bookchapter_result.group(1).split(' and ')
                for author in authors:
                    if ',' in author:
                        author_split = author.split(',')
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[1].strip(), last_name=author_split[0].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=book_chapter)
                    else:
                        author_split = author.rsplit(' ', 1)
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[0].strip(), last_name=author_split[1].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=book_chapter)
                
                publisher, created = models.publisher.objects.get_or_create(publisher_name=bookchapter_result.group(4).strip())
                doc_publisher, created = models.document_publisher.objects.get_or_create(publisher=publisher, document=book_chapter)
                
                publication_place, created = models.publication_place.objects.get_or_create(place=bookchapter_result.group(5).strip())
                doc_publication_place, created = models.document_publication_place.objects.get_or_create(publication_place=publication_place, document=book_chapter)
                
                publication_date, created = models.pdate.objects.get_or_create(date=datetime.datetime.strptime(bookchapter_result.group(6).strip(), '%Y'))
                doc_publication_date, created = models.document_date.objects.get_or_create(date=publication_date, document=book_chapter)
                
                publication_type, created = models.ptype.objects.get_or_create(type='Book chapter')
                doc_document_type, created = models.document_type.objects.get_or_create(dtype=publication_type, document=book_chapter)
                
                line.extract()

    html = soup.prettify()
    
    return HttpResponse(html)