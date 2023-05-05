def populate_data():
    from reviews.models import Publisher, Contributor, Book, BookContributor, Review
    from django.contrib.auth.models import User
    from datetime import date, datetime
    fileRead = open('WebDevWithDjangoData.csv', 'r')
    contentType = ""

    lines = fileRead.readlines()
    for line in lines:
        row = line.strip().split(",")
        row1 = list(filter(None, row))
        if len(row1) > 0 and row1[0] == "content:Publisher":
            contentType = 'publisher'

        if len(row1) > 0 and row1[0] == 'content:Book':
            contentType = 'book'

        if len(row1) > 0 and row1[0] == 'content:Contributor':
            contentType = 'contributor'

        if len(row1) > 0 and row1[0] == 'content:BookContributor':
            contentType = 'book-contributor'

        if len(row1) > 0 and row1[0] == 'content:Review':
            contentType = 'review'

        if contentType == 'publisher' and len(row1) > 2 and row1[0] != 'publisher_name' and \
                row1[1] != 'publisher_website' and row1[2] != 'publisher_email':
            name = row1[0]
            website = row1[1]
            email = row1[2]
            Publisher.objects.create(name=name, website=website, email=email)

        if contentType == 'book' and len(row1) > 3 and row1[0] != 'book_title' and \
                row1[1] != 'book_publication_date' and row1[2] != 'book_isbn' and row1[3] != 'book_publisher_name':
            title = row1[0]
            year, month, day = row1[1].split('/')
            isbn = row1[2]
            bookPubName = Publisher.objects.get(name=row1[3])
            Book.objects.create(title=title, publication_date=date(year=int(year), month=int(month), day=int(day)), isbn=isbn, publisher=bookPubName)

        if contentType == 'contributor' and len(row1) > 2 and row1[0] != 'contributor_first_names'\
                and row1[1] != 'contributor_last_names' and row1[2] != 'contributor_email':
            fname = row1[0]
            lname = row1[1]
            email = row1[2]
            Contributor.objects.create(first_names=fname, last_names=lname, email=email)

        if contentType == 'book-contributor' and len(row1) > 2 and row1[0] != 'book_contributor_book'\
                and row1[1] != 'book_contributor_contributor' and row1[2] != 'book_contributor_role':
            book = Book.objects.get(title=row1[0])
            contributor = Contributor.objects.get(email=row1[1])
            role = row1[2]
            BookContributor.objects.create(book=book, contributor=contributor, role=role)
            book.contributors.add(contributor,  through_defaults={'role': role})

        if contentType == 'review' and len(row1) > 3 and row1[0] != 'review_content' \
                and row1[1] != 'review_rating' and row1[2] != 'review_date_created' \
                and row1[3] != 'review_date_edited' and row1[4] != 'review_creator' and row1[5] != 'review_book':
            content = row1[0]
            rating = row1[1]
            dateCreated = row1[2]
            dateEdited = row1[3]
            creator = row1[4]
            book = Book.objects.get(title=row1[5])

            #DateCreated Splits
            x = dateCreated.split(" ")
            date = x[0].split("-")
            time = x[1].split(":")
            second = time[2].split(".")
            yearC = int(date[0])
            monthC = int(date[1])
            dayC = int(date[2])
            hourC = int(time[0])
            minuteC = int(time[1])
            secC = int(second[0])
            micsecC = int(second[1])

            #DateEdited Splits
            y = dateEdited.split(" ")
            dateE = y[0].split("-")
            timeE = y[1].split(":")
            secondE = timeE[2].split(".")
            yearE = int(dateE[0])
            monthE = int(dateE[1])
            dayE = int(dateE[2])
            hourE = int(timeE[0])
            minuteE = int(timeE[1])
            secE = int(secondE[0])
            micsecE = int(secondE[1])

            #Creator FK
            username = creator.split("@")
            user = User.objects.create_user(username=username[0], email=creator)

            Review.objects.create(content=content, rating=int(rating),
                                  date_created=datetime(year=yearC, month=monthC, day=dayC, hour=hourC, minute=minuteC, second=secC, microsecond=micsecC),
                                  date_edited=datetime(year=yearE, month=monthE, day=dayE, hour=hourE, minute=minuteE, second=secE, microsecond=micsecE),
                                  creator=user, book=book)
    fileRead.close()
