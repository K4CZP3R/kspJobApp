import kspDebug, json, base64, pathlib, datetime, uuid, random
from urllib.parse import quote
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
import requests
from time import sleep
class KspConfig:
    configFile = "config.json"
    def __init__(self, configFile=configFile):
        self.debug = kspDebug.kspDebug("KspConfig")
    def readConfig(self):
        self.debug.out("Reading config...")
        with open(self.configFile, "r") as read_file:
            try:
                return json.load(read_file)
            except:
                return None
    def readValue(self, key):
        self.debug.out("Reading key '{}'".format(key))
        with open(self.configFile, "r") as read_file:
            try:
                return json.load(read_file)[key]
            except:
                return None
    def createDummyJson(self):
        if not pathlib.Path(self.configFile).exists():
            self.debug.out("Creating dummy (empty) json",level=kspDebug.WARN)
            write_file = open(self.configFile, "w")
            write_file.write("{}")
            write_file.close()
    def saveValue(self, key, value):
        #self.debug.out("Saving '{key}':'{value}'".format(key=key, value=value))

        self.createDummyJson()            
        read_file = open(self.configFile, "r")
        file_dict = json.load(read_file)
        read_file.close()
        file_dict[key] = value
        write_file = open(self.configFile, "w")
        json.dump(file_dict, write_file, indent=4)
        write_file.close()
class KspHttp:
    class Session:
        def __init__(self):
            self.ses = requests.Session()
            
            self.certVerify = False
            self.allowRedirects = True

        def setCertVerify(self, value):
            self.certVerify = value
        def setUrl(self, url):
            self.url = url
        def popCookie(self, cookieKey):
            self.ses.cookies.pop(cookieKey)
        def bulkAddHeaders(self, headersArray):
            for header in headersArray:
                self.addHeader(header)
        def addHeader(self, headerDict):
            self.ses.headers.update(headerDict)
        def popHeader(self, headerKey):
            self.ses.headers.pop(headerKey)
        def getHeaders(self):
            return self.ses.headers.values()
        def setData(self, data):
            self.data = data
        def setAllowRedirects(self, value):
            self.allowRedirects = value
        def POST(self):
            return self.ses.post(
                url=self.url,
                data=self.data,
                allow_redirects=self.allowRedirects,
                verify=self.certVerify
            )
        def GET(self):
            return self.ses.get(
                url=self.url,
                allow_redirects=self.allowRedirects,
                verify=self.certVerify
            )
    class Url:
        def escape(self, value, safe=''):
            return quote(value, safe=safe)
        def parse_url(self, url):
            return parse_qs(urlparse(url).query)
        def fix_loggedin_url(self, url):
            magic = "LoginSuccess.html"
            magic = url.index(magic)+len(magic)
            url = list(url)
            url[magic] = "?"
            return "".join(url)
class KspWebDriver:
    def __init__(self):
        self.debug = kspDebug.kspDebug("webDriver")
        self.driver = webdriver.Chrome()
    def goTo(self, url):
        self.debug.out("Getting '{}'".format(url))
        self.driver.get(url)
    def getCookies(self, url):
        return self.driver.get_cookies()
    def enterInElement(self, element_id, value):
        self.driver.find_element_by_id(element_id).send_keys(value)
    def executeJs(self, value):
        self.driver.execute_script(value)
    def getUrl(self):
        return self.driver.current_url
    def exit(self):
        self.debug.out("Closing!", level=kspDebug.WARN)
        self.driver.close()
class DecompiledApp:
    class UserLogOnViewModel:
        def __init__(self):
            self.debug = kspDebug.kspDebug("UserLogOnViewModel")
        def InitializeAuthenticator(self):
            environmentSettings__Simplified = DecompiledApp.EnvironmentSettings__Simplified()
            self.dvoa2a = DecompiledApp.DeVriesOAuth2Authenticator("957995625457764", "read", environmentSettings__Simplified.PublicaionIdentityEndpoint() + "connect/v2/authorize",environmentSettings__Simplified.PublicaionIdentityEndpoint()+"LoginSuccess.html")
        def kspGetLoginLink(self):
            return self.dvoa2a.kspGetInitialUrl()
        def kspGetAuthInfoFromUrl(self, url):
            self.debug.out("Fixing url...")
            url = KspHttp.Url().fix_loggedin_url(url)

            self.debug.out("Parsing url...")
            url_parsed = KspHttp.Url().parse_url(url)

            return {
                'access_token': url_parsed['access_token'][0],
                'token_type': url_parsed['token_type'][0]
            }
    class DeVriesOAuth2Authenticator:
        def __init__(self, clientId, scope, authorizeUrl, redirectUrl):
            self._scope = scope
            self._redirectUrl = redirectUrl
            self._authorizeUrl = authorizeUrl
            self.Initialize(clientId, scope)
        
        def Initialize(self, clientId, scope):
            self._clientId = clientId
            self._scope = scope

            chArray = list("\0" * 16)
            for index in range(0, len(chArray)):
                chArray[index] = chr(random.randint(97, 123))
            self._requestState = ''.join(chArray)
        
        def kspGetInitialUrl(self):
            _deviceInfoService = DecompiledApp.DeviceInfoService()
            _url = KspHttp.Url()

            return "{0}?client_id={1}&redirect_uri={2}&response_type={3}&scope={4}&state={5}&device_info={6}".format(
                self._authorizeUrl,
                _url.escape(self._clientId),
                _url.escape(self._redirectUrl),
                "token",
                _url.escape(self._scope),
                self._requestState,
                _deviceInfoService.RetrieveToken()
            )
    class AndroidDeviceInfoService:
        def RetrieveAppFunctionalVersion(self):
            return "7.3.0"
        def RetrieveAppTechnicalVersion(self):
            return "40"
        def RetrieveOperatingSystemName(self):
            return "Android"
        def RetrieveOperatingSystemVersion(self):
            return "9"
        def RetrieveDeviceModel(self):
            return "{manu} {model}".format(manu="OnePlus", model="ONEPLUS A6003")
        def RetrieveAppName(self):
            return "job app"
    class DeviceInfoService:
        def RetrieveToken(self):
            return "134c74a4-8fce-11e9-b652-e0d55e879064"
            #return str(uuid.uuid4()) #hardcoded for now
        def RetrieveDeviceInfo(self):
            return json.dumps({
                'Token': self.RetrieveToken(),
                'AppName': DecompiledApp.AndroidDeviceInfoService().RetrieveAppName(),
                'AppFunctionalVersion': DecompiledApp.AndroidDeviceInfoService().RetrieveAppFunctionalVersion(),
                'AppTechnicalVersion': DecompiledApp.AndroidDeviceInfoService().RetrieveAppTechnicalVersion(),
                'OperatingSystemName': DecompiledApp.AndroidDeviceInfoService().RetrieveOperatingSystemName(),
                'OperatingSystemVersion': DecompiledApp.AndroidDeviceInfoService().RetrieveOperatingSystemVersion(),
                'DeviceModel': DecompiledApp.AndroidDeviceInfoService().RetrieveDeviceModel()
            })
    class EnvironmentSettings__Simplified:
        def PublicaionIdentityEndpoint(self):
            return "https://api.devrieswfm.com/identity/"
    class AccessTokenPayload:
        def __init__(self, base64EncodedAccessToken):
            self.debug = kspDebug.kspDebug("AccessTokenPayload")
            self.ParseToken(base64EncodedAccessToken)
            self.ParseProperties()

        def ParseToken(self, base64EncodedAccessToken):
            token_splited = base64EncodedAccessToken.split(".")
            if len(token_splited) < 3:
                self.debug.out("Token must contain at least 3 parts", level=kspDebug.WARN)
            self.rawData = json.loads(base64.b64decode(token_splited[1] + "=" * (-len(token_splited[1]) % 4)).decode("UTF-8"))

        def ParseProperties(self):
            nameIdentifier = self.rawData['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier']
            expiry = str(self.EpochTimeToDateTime(int(self.rawData['exp'])))
            employeeId = int(self.rawData['urn:www-devrieswfm-com:security/claims/employee'])
            clientCode = self.rawData['urn:www-devrieswfm-com:security/claims/clientcode']
            shopId = self.rawData['urn:www-devrieswfm-com:security/claims/organization']
            publicationUrl = self.rawData['urn:www-rrwfm-com:api/claims/publicationurl']

            source = self.rawData['urn:www-devrieswfm-com:security/claims/publicationsubscription']
            subscriptions = list()
            for s in source:
                subscriptions.append(s)
            

            KspConfig().saveValue("nameIdentifier", nameIdentifier)
            KspConfig().saveValue("expiry", expiry)
            KspConfig().saveValue("employeeId", employeeId)
            KspConfig().saveValue("clientCode", clientCode)
            KspConfig().saveValue("shopId", shopId)
            KspConfig().saveValue("publicationUrl", publicationUrl)
            KspConfig().saveValue("subscriptions", subscriptions)
        
        def EpochTimeToDateTime(self, secondsSinceUnixEpoch):
            return datetime.datetime.fromtimestamp(secondsSinceUnixEpoch)

class KspJobApp_data:
    js_fakeDeviceInfo = 'document.getElementById("deviceInfo").value = \'{}\''
    js_clickButton = 'document.getElementsByTagName("button")[0].click();'
    headersToPop = ['User-Agent', 'Accept']
    headersToAdd = [{'Content-Type': 'application/json; charset=utf-8'}]
class KspJobApp:
    def __init__(self):
        self.debug = kspDebug.kspDebug("main")
    def kspConfigureSession(self, session):
        self.debug.out("Preparing session to be used in JobApp env")
        self.debug.out("Popping unused headers")
        for header in KspJobApp_data.headersToPop:
            self.debug.out("[!] Popped '{}'".format(header))
            session.popHeader(header)
        self.debug.out("Adding headers")
        for header in KspJobApp_data.headersToAdd:
            self.debug.out("[!] Added '{}'".format(header))
            session.addHeader(header)
        return session
    def kspSchedule_getPeriod(self, year, week):
        config_dict = KspConfig().readConfig()

        api_session = self.kspConfigureSession(KspHttp.Session())
        publicationUrl = config_dict['publicationUrl']
        access_token = config_dict['access_token']
        token_type = config_dict['token_type']
        shopId = config_dict['shopId']
        employeeId = config_dict['employeeId']
        
        self.debug.out("Adding secure/default headers")
        api_session.bulkAddHeaders([
            {"Authorization": "{} {}".format(token_type, access_token)},
            {"x-DeviceInformation": DecompiledApp.DeviceInfoService().RetrieveDeviceInfo()},
            {"Accept-Language": "en-US"}
        ])
        
        self.debug.out("Getting schedule for year:{}|week:{}".format(year, week))
        api_session.setUrl("{}/schedule/employees/{}/{}/{}/True".format(
            publicationUrl,employeeId, year, week
        ))

        resp_1 = api_session.GET()

        self.debug.out("Getting replacements for year:{}|week:{}".format(year, week))
        api_session.setUrl("{}/replacement/{}/{}/{}/{}".format(
            publicationUrl, shopId, employeeId, year, week
        ))

        resp_2 = api_session.GET()

        return {
            'schedule': resp_1.json(),
            'replacement': resp_2.json()
        }

        


    def kspSchedule_getPeriods(self):
        config_dict = KspConfig().readConfig()

        api_session = self.kspConfigureSession(KspHttp.Session())
        publicationUrl = config_dict['publicationUrl']
        access_token = config_dict['access_token']
        token_type = config_dict['token_type']
        shopId = config_dict['shopId']
        employeeId = config_dict['employeeId']

        self.debug.out("Getting av. schedules")
        api_session.setUrl("{}/schedule/shops/{}/employees/{}".format(
            publicationUrl, shopId, employeeId
        ))

        self.debug.out("Adding secure/default headers")
        api_session.bulkAddHeaders([
            {"Authorization": "{} {}".format(token_type, access_token)},
            {"x-DeviceInformation": DecompiledApp.DeviceInfoService().RetrieveDeviceInfo()},
            {"Accept-Language": "en-US"}
        ])
        self.debug.out("GET!")
        resp_1 = api_session.GET()
        return resp_1.json()


    def kspOpenApp(self):
        config_dict = KspConfig().readConfig()

        self.debug.out("Initializing a new Http session")
        api_session = self.kspConfigureSession(KspHttp.Session())

        token_type = config_dict['token_type']
        access_token = config_dict['access_token']
        employeeId = config_dict['employeeId']
        publicationUrl = config_dict['publicationUrl']
        
        #reportAppVersion
        self.debug.out("Reporting app version to server!")
        api_session.setUrl("{}/user/{}/v2/version".format(
            publicationUrl, employeeId
        ))

        self.debug.out("Adding secure/default headers")
        api_session.bulkAddHeaders([
            {"Authorization": "{} {}".format(token_type, access_token)},
            {"x-DeviceInformation": DecompiledApp.DeviceInfoService().RetrieveDeviceInfo()},
        ])
        api_session.setData(DecompiledApp.DeviceInfoService().RetrieveDeviceInfo())

        self.debug.out("Making POST request")
        if api_session.POST().status_code == 200:
            self.debug.out("OK!")
        else:
            self.debug.out("NOT OK!", level=kspDebug.WARN)
        

        #isFeatureApplicable
        self.debug.out("Checking if feature is applicable! (dummy)")
        api_session.setUrl("{}/is-feature-applicable/Freizeit/".format(
            publicationUrl
        )) 
        #self.debug.out("resp: '{}'".format(api_session.GET().text))

        #accessTokenRenew
        self.debug.out("Renewing access token!")
        environmentSettings__Simplified = DecompiledApp.EnvironmentSettings__Simplified()
        api_session.setUrl("{}connect/v2/accessTokenRenew".format(environmentSettings__Simplified.PublicaionIdentityEndpoint()))
        #self.debug.out("resp: '{}'".format(api_session.GET().json()))

        #connectAuthorize
        self.debug.out("Authorizing session")
        api_session.setUrl("{}/AuthServer/connect/authorize".format(
            publicationUrl
        ))

        resp = api_session.GET()
        #self.debug.out("resp: '{}'".format(resp.json()))
        self.debug.out("Saving new valid access token")
        KspConfig().saveValue("access_token", resp.json()['access_token'])
        KspConfig().saveValue("token_type", resp.json()['token_type'])
        
        self.debug.out("Simulating app delay")
        sleep(random.randint(5, 15)/10)
        self.debug.out("You can now use other APIs!")

    def kspLogin(self, username, password):
        self.debug.out("Will login as '{}'".format(username))

        self.debug.out("Initializing authenticator... [1/2]")
        userLogOnViewModel = DecompiledApp.UserLogOnViewModel()
        userLogOnViewModel.InitializeAuthenticator()
        self.debug.out("Getting login link... [2/2]")
        login_link = userLogOnViewModel.kspGetLoginLink()
        self.debug.out("Login link: '{}'".format(login_link))

        self.debug.out("Initializing webdriver")
        self.wd = KspWebDriver()

        self.debug.out("Redirecting to login link")
        self.wd.goTo(login_link)

        self.debug.out("Entering credentials...")
        self.wd.enterInElement("username", username)
        self.wd.enterInElement("password", password)
        self.debug.out("Faking device info...")
        self.wd.executeJs(KspJobApp_data.js_fakeDeviceInfo.format(DecompiledApp.DeviceInfoService().RetrieveDeviceInfo()))
        self.debug.out("Logging in...")
        self.wd.executeJs(KspJobApp_data.js_clickButton)

        sleep(0.75)

        self.debug.out("Getting url with auth info...")
        auth_url = self.wd.getUrl()
        self.wd.exit()

        self.debug.out("Deriving auth info...")
        auth_info = userLogOnViewModel.kspGetAuthInfoFromUrl(auth_url)

        self.debug.out("Saving auth info to config...")
        KspConfig().saveValue("access_token", auth_info['access_token'])
        KspConfig().saveValue("token_type", auth_info['token_type'])

        self.debug.out("Deriving info from access_token")
        DecompiledApp.AccessTokenPayload(auth_info['access_token'])
        self.debug.out("Done!")

KspJobApp().kspOpenApp()
periods = KspJobApp().kspSchedule_getPeriods()

current_period = periods['CurrentPeriod']

current_period = KspJobApp().kspSchedule_getPeriod(current_period['Year'], current_period['WeekNumber'])

print(json.dumps(current_period, indent=4, sort_keys=True))