from upstox_api.api import *
from datetime import datetime
from pprint import pprint
import os, sys
from tempfile import gettempdir
from requests import Request
import json
from django.shortcuts import redirect
try: input = raw_input
except NameError: pass
import mechanicalsoup, requests
from mechanicalsoup.utils import *
from w3lib.url import url_query_parameter
from .models import *
from django.core.exceptions import *

u = None
s = None

break_symbol = '@'

profile = None

def main(user_id, password, birthyear , selection, userprofile):
    global s, u

    logged_in = False
    stored_api_key = userprofile.api_key
    stored_access_token = userprofile.access_token
    if stored_access_token is not None and stored_api_key is not None:
        try:
            u = Upstox(stored_api_key, stored_access_token)
            logged_in = True
        except requests.HTTPError as e:
            print e
    if logged_in is False:
        stored_api_key = userprofile.api_key
        if stored_api_key is not None:
            api_key = stored_api_key
        else:
            return {'is_error': True, 'errorMsg': 'api_key not present in user profile'}
        stored_api_secret = userprofile.secret_key
        if stored_api_secret is not None:
            api_secret = stored_api_secret
        else:
            return {'is_error': True, 'errorMsg': 'secret_key not present in user profile'}
        stored_redirect_uri = userprofile.redirect_url
        if stored_redirect_uri is not None:
            redirect_uri = stored_redirect_uri
        else:
            return {'is_error': True, 'errorMsg': 'redirect_uri not present in user profile'}
        s = Session(api_key)
        s.set_redirect_uri(redirect_uri)
        s.set_api_secret(api_secret)

        #print('URL: %s\n' % s.get_login_url())

        link =s.get_login_url()
        try :
            code = getAccessToken(link, user_id, password, birthyear ,  userprofile)
        except LinkNotFoundError as e:
                #print 'Value code cannot be None. LinkNotFoundError while accessing Upstox API: [%s]' % e
                return {'is_error': True, 'errorMsg': 'Value code cannot be None. api_key/secret_key/redirect_uri is invalid for accessing Upstox API: [%s]' % e}
        except AttributeError as e:
                #print 'Value code cannot be None. AttributeError while accessing Upstox API: [%s]' % e
                return {'is_error': True, 'errorMsg': 'Value code cannot be None. api_key/secret_key/redirect_uri is invalid for accessing Upstox API: [%s]' % e}
        except RuntimeError as e :
                return {'is_error': True, 'errorMsg': e}
        userprofile.access_token = code
        userprofile.save()
        if code is not None:
            s.set_code(code)
        else :
            return {'is_error': True, 'errorMsg': 'Value code cannot be None. api_key/secret_key/redirect_uri is invalid for accessing Upstox API:'}
        try:
            access_token = s.retrieve_access_token()
        except SystemError as se:
            #print('Uh oh, there seems to be something wrong. Error: [%s]' % se)
            return {'is_error': True, 'errorMsg': 'Uh oh, there seems to be something wrong. Error from Upstox API: [%s]' % se}
        write_key_to_settings('access_token', access_token)
        u = Upstox(api_key, access_token)

    return show_home_screen(selection)

def show_home_screen(selection):
    global s, u
    global profile
    selection = int(selection)
    #clear_screen()
    if selection == 1:
        load_profile()
        return profile
    elif selection == 2:
        return u.get_balance()
    elif selection == 3:
        return u.get_positions()
    elif selection == 4:
        return u.get_holdings()
    elif selection == 5:
        return u.get_order_history()
    elif selection == 6:
        product = select_product()
        if product is not None:
            return u.get_live_feed(product, LiveFeedType.LTP)
    elif selection == 7:
        product = select_product()
        if product is not None:
            return u.get_live_feed(product, LiveFeedType.Full)
    elif selection == 8:
        socket_example()
    elif selection == 9:
        sys.exit(0)



def load_profile():
    global profile
    # load user profile to variable
    profile = u.get_profile()


def select_product():
    global u
    exchange = select_exchange()
    product = None
    clear_screen()
    while exchange is not None:
        u.get_master_contract(exchange)
        product = find_product(exchange)
        clear_screen()
        if product is not None:
            break
        exchange = select_exchange()

    return product

def find_product(exchange):
    found_product = False
    result = None

    while not found_product:
        query = input('Type the symbol that you are looking for. Type %s to go back:  ' % break_symbol)
        if query.lower() == break_symbol:
            found_product = True
            result = None
            break
        results = u.search_instruments(exchange, query)
        if len(results) == 0:
            print('No results found for [%s] in [%s] \n\n' % (query, exchange))
            break
        else:
            for index, result in enumerate(results):
                if index > 9:
                    break
                print ('%d. %s' % (index, result.symbol))
            selection = input('Please make your selection. Type %s to go back:  ' % break_symbol)

            if query.lower() == break_symbol:
                found_product = False
                result = None
                break

            try:
                selection = int(selection)
            except ValueError:
                found_product = False
                result = None
                break

            if 0 <= selection <= 9 and len(results) >= selection + 1:
                found_product = True
                result = results[selection]
                break

            found_product = False

    return result

def select_exchange():
    global profile
    if profile is None:
        load_profile()

    back_to_home_screen = False
    valid_exchange_selected = False

    while not valid_exchange_selected:
        print('** Live quote streaming example **\n')
        for index, item in enumerate(profile[u'exchanges_enabled']):
            print ('%d. %s' % (index + 1, item))
        print ('9. Back')
        print('\n')

        selection = input('Select exchange: ')

        try:
            selection = int(selection)
        except ValueError:
            break

        if selection == 9:
            valid_exchange_selected = True
            back_to_home_screen = True
            break

        selected_index = selection - 1

        if 0 <= selected_index < len(profile[u'exchanges_enabled']):
            valid_exchange_selected = True
            break

    if back_to_home_screen:
        return None

    return profile[u'exchanges_enabled'][selected_index]


def socket_example():
    print('Press Ctrl+C to return to the main screen\n')
    u.set_on_quote_update(event_handler_quote_update)
    u.get_master_contract('NSE_EQ')
    try:
        u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), LiveFeedType.Full)
    except:
        pass
    try:
        u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE'), LiveFeedType.LTP)
    except:
        pass
    u.start_websocket(False)


def event_handler_quote_update(message):
    pprint("Quote Update: %s" % str(message))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def write_key_to_settings(key, value):
    filename = os.path.join(gettempdir(), 'interactive_api.json')
    try:
        file = open(filename, 'r')
    except IOError:
        data = {"api_key" : "", "api_secret" : "", "redirect_uri" : "", "access_token" : ""}
        with open(filename, 'w') as output_file:
            json.dump(data, output_file)
    file = open(filename, 'r')
    try:
        data = json.load(file)
    except:
        data = {}
    data[key] = value
    with open(filename, 'w') as output_file:
        json.dump(data, output_file)

def read_key_from_settings(key):
    filename = os.path.join(gettempdir(), 'interactive_api.json')

    try:
		file = open(filename, 'r')
    except IOError:
        file = open(filename, 'w')
    file = open(filename, 'r')
    try:
        data = json.load(file)
        return data[key]
    except:
        pass
    return None

def getAccessToken(link, user_id, password, birthyear ,  userprofile):
    code = None
    #try :
    r = requests.get(link, allow_redirects=True)
    #print(r.text.encode('utf-8'))
    # Connect to duckduckgo
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(link)

    # Fill-in the search form
    form = browser.select_form()

    browser["apiKey"] = userprofile.api_key
    browser["username"] = user_id
    browser["password"] = password
    browser["password2fa"] = birthyear
    resp = browser.submit_selected()
    print(resp)
    if resp.status_code == 200 :
        #print '200'
        page = browser.get_current_page()
        #print page
        res = page.find("p", class_="error-msg")
        if res is not None:
            raise RuntimeError(res.getText())
    form1 = browser.select_form()
    browser.get_current_form().choose_submit_by_value('Accept')
    resp = browser.submit_selected();
    print(resp)
    code = url_query_parameter(resp.url, 'code')
    #print(code)
    return code


def getUserRole(username):
    try:
        go  = UserRole.objects.get(user_id=username)
    except ObjectDoesNotExist:
        go = None
    return go

def getUserProfile(username):
    try:
        go  = UserProfile.objects.get(user_id=username)
    except ObjectDoesNotExist:
        go = None
    return go
