import datetime
import os.path
import time
import requests
import os
import pickle
from http.cookiejar import MozillaCookieJar

from datetime import datetime

from pyinstalive import helpers

from . import logger
from . import globals
from . import api
from .constants import Constants

class Session:
    def _save_session(self):
        with open(self.session_file, "wb") as f:
            pickle.dump(self.session, f)

    def _load_session(self):
        with open(self.session_file, "rb") as f:
            return pickle.load(f)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session_file = None
        self.session = None
        self.cookies = None
        self.expires_epoch = None
        self.proxy = None

    def authenticate(self, username=None, password=None):
        try:
            if globals.config.proxy and not self.proxy:
                logger.binfo("Checking if the proxy is working.")
                self.proxy = helpers.test_proxy()
                if self.proxy:
                    logger.info("The proxy is working properly.")
                else:
                    logger.warn("The proxy check failed, falling back to default connection.")
                logger.separator()

            login_success = False
            if username and password:
                self.username = username
                self.password = password
                logger.binfo("The default login credentials have been overridden.")
                logger.separator()
            
            self.session_file = globals.config.session_file if globals.config.session_file and os.path.isfile(globals.config.session_file) else os.path.join(os.path.dirname(globals.config.config_path), "{}.dat".format(self.username))
            self.cookies_file = globals.config.cookies_file if globals.config.cookies_file and os.path.isfile(globals.config.cookies_file) else os.path.join(os.path.dirname(globals.config.config_path), "{}.txt".format(self.username))
            
            if os.path.isfile(self.cookies_file):
                logger.info(f"Cookies file detected: {self.cookies_file}.")
                
                self.session = requests.Session()
                cookie_jar = MozillaCookieJar(self.cookies_file)
                cookie_jar.load(self.cookies_file, ignore_discard=True, ignore_expires=True)
                self.session.cookies.update(cookie_jar)
                
                self.session.headers = Constants.BASE_HEADERS
    
                self._save_session()
                logger.separator()
                logger.info("Successfully created a new login session file: {:s}".format(os.path.basename(self.session_file)))
                for cookie in list(self.session.cookies):
                    if cookie.name == "csrftoken":
                        self.session.headers.update({"x-csrftoken": self.session.cookies["csrftoken"]})
                        self.expires_epoch = cookie.expires
                login_success = True

            
            else:
                logger.warn("Could not find an existing cookies file: {}".format(os.path.basename(self.cookies_file)))
    
                if not os.path.isfile(self.session_file):
                    logger.warn("Could not find an existing login session file: {:s}".format(os.path.basename(self.session_file)))
                    logger.warn("A new login session file will be created upon successful login.")

                    self.session = requests.Session()
                    self.session.headers = Constants.BASE_HEADERS

                    

                    if globals.config.proxy and self.proxy:
                        self.session.proxies = self.proxy

                    self.session.headers.update({"x-csrftoken": api.get_csrf_token()})

                    login_result = api.do_login()
                    if login_result.get("authenticated", None):
                        self._save_session()
                        logger.separator()
                        logger.info("Successfully created a new login session file: {:s}".format(os.path.basename(self.session_file)))
                        for cookie in list(self.session.cookies):
                            if cookie.name == "csrftoken":
                                self.expires_epoch = cookie.expires
                        login_success = True
                    else:
                        logger.separator()
                        if login_result.get("user") == False:
                            logger.error("Could not login: The account does not exist.")
                        elif login_result.get("message", '') == "checkpoint_required":
                            logger.error("Could not login: The action was flagged as suspicious by Instagram.")
                            logger.error("Complete the security checkpoint on another device and try again.")
                        else:
                            logger.error("Could not login: Ensure your credentials are correct and try again.")
                        logger.separator()
                        login_success = False
                else:
                    self.session = self._load_session()
                    if globals.config.proxy and self.proxy:
                        self.session.proxies = self.proxy
                    logger.info("An existing login session file was found: {}".format(os.path.basename(self.session_file)))
                    logger.info("Checking the validity of the saved login session.")

                    for cookie in list(self.session.cookies):
                        if cookie.name == "csrftoken":
                            self.expires_epoch = cookie.expires

                    if int(self.expires_epoch) <= int(time.time()):
                        os.remove(self.session_file)
                        self.session_file = None

                        logger.warn("The login session file has expired and has been deleted.")
                        logger.warn("A new login session file will be created upon successful login.")

                        time.sleep(1)
                        self.authenticate(username, password)
                        return
                    else:
                        login_state = api.get_login_state()
                        if login_state.get("entry_data", {}) != {}:
                            if login_state.get("entry_data", {}).get("Challenge", None) != None:
                                logger.separator()
                                logger.error("The session was flagged as suspicious by Instagram.")
                                logger.error("Complete the security checkpoint on another device and try again.")
                                logger.separator()
                                login_success = False
                            else:
                                logger.error("The login session file is no longer valid.")
                                logger.error("Unspecified error. Delete the login session file and try again.")
                                logger.separator()
                                login_success = False
                        else:
                            login_success = True

            if login_success:
                if self.session.cookies["csrftoken"] != self.session.headers.get("x-csrftoken"):
                    self.session.cookies.set("csrftoken", self.session.headers.get("x-csrftoken"), domain=".instagram.com", expires=self.expires_epoch)
                logger.separator()
                logger.info('Successfully logged in using account: {:s}'.format(str(self.username)))

                expiry_date = datetime.fromtimestamp(self.expires_epoch).strftime('%m-%d-%Y at %I:%M:%S %p')
                logger.info("The login session file will expire on: {:s}".format(expiry_date))

                logger.separator()
                return True
            else:
                return False
        except Exception as e:
            logger.error('Could not login: {:s}'.format(str(e)))
            logger.separator()
            return False
        except KeyboardInterrupt:
            logger.separator()
            logger.binfo('The process was aborted by the user.')
            logger.separator()
            return False
