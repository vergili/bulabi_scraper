import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging


class EmailNotification(object):

    @staticmethod
    def send_email(message, title, recipients):
        print "Sending mail..........."

        # TODO create an email
        gmailUser = 'automated.search@gmail.com'
        gmailPassword = 'automated.2016'

        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = ",".join(recipients)

        msg['Subject'] = title
        msg.attach(MIMEText(message))

        """
        visit and update  security option for gmail
        https://www.google.com/settings/security/lesssecureapps
        """
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipients, msg.as_string())
        mailServer.close()
        print "Mail sent"

    def send_spider_error_email(self, spider):
        error = 0
        try:
            error = int(spider.crawler.stats._stats['log_count/ERROR'])
        except KeyError:
            pass

        finish_reason = 'NA'
        try:
            finish_reason = spider.crawler.stats._stats['finish_reason']
        except KeyError:
            pass

        item_scraped_count = 0
        try:
            item_scraped_count = int(spider.crawler.stats._stats['item_scraped_count'])
        except KeyError:
            pass

        logging.info("Finish Reason: {0} - Error: {1} - Item Scraped: {2}".
                     format(finish_reason, str(error), str(item_scraped_count)))

        if 'finished' not in finish_reason or error > 0 or item_scraped_count < 1:

            scrapy_job_id = 'NA'
            try:
                scrapy_job_id = os.environ['SCRAPY_JOB']
            except KeyError:
                pass

            title = 'ERROR ' + str(spider.name)
            message = 'There are some ERROR on ' + str(spider.name) + ' \n' \
                      ' job id: ' + str(scrapy_job_id) + ' \n' + \
                      ' scraped items: ' + str(item_scraped_count)

            email_recipients = ["vergili@cern.ch" ]
            self.send_email(message, title, email_recipients)
