from email.mime.text import MIMEText
import smtplib
import subprocess
import ConfigParser
import sys
import os

def read_config_option(config, section, option, default_option=None):
    ''' Read the config file. If the option/section is not present, return the default_option
    '''
    try:
        val = config.get(section, option)
        if val.lower() == 'true':
            val = True
        elif val.lower() == 'false' or val.lower() == 'none':
            val = False
        elif not val:
            val = default_option
        return val
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        return default_option
# end read_config_option

def send_mail(config_file, file_to_send, report_details):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    report_config = ConfigParser.ConfigParser()
    report_config.read(report_details)
    distro_sku = report_config.get('Test','Distro_Sku')
    smtpServer = read_config_option(config, 'Mail', 'server')
    smtpPort = read_config_option(config, 'Mail', 'port')
    mailSender = read_config_option(config, 'Mail', 'mailSender', 'contrailbuild@juniper.net')
    mailTo = read_config_option(config, 'Mail', 'mailTo')
    if 'EMAIL_SUBJECT' in os.environ:
        logScenario = os.environ.get('EMAIL_SUBJECT')
    else:
        logScenario = read_config_option(config, 'Basic', 'logScenario')

    if not mailTo or not smtpServer or not smtpPort:
        print 'Mail destination not configured. Skipping'
        return True
    fp = open(file_to_send, 'rb')
    msg = MIMEText(fp.read(), 'html')
    fp.close()

    msg['Subject'] = '[Build %s] ' % (
         distro_sku) + logScenario + ' Report'
    msg['From'] = mailSender
    msg['To'] = mailTo

    s = None
    try:
        s = smtplib.SMTP(smtpServer, smtpPort)
    except Exception, e:
        print "Unable to connect to Mail Server"
        return False
    s.ehlo()
    try:
        s.sendmail(mailSender, mailTo.split(","), msg.as_string())
        s.quit()
    except smtplib.SMTPException, e:
        print 'Error while sending mail'
        return False
    return True
# end send_mail

if __name__ == "__main__":
    #send_mail('sanity_params.ini','report/junit-noframes.html') 
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
