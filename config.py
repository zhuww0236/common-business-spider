# -*- coding: utf-8 -*-

BASE_UPLOAD_HOST = 'http://admin.tkcat.cn/apider/storeUp'
BASE_UPLOAD_ITMES_HOST = 'http://admin.tkcat.cn/apider/storeGoodsSaleInfo'
BASE_UPLOAD_COUPONS_HOST = 'http://admin.tkcat.cn/apider/storeCoupon'
# BASE_UPLOAD_COUPONS_HOST = 'http://10.4.250.227:8080/apider/storeCoupon'
BASE_GET_ITEMS_HOST = 'http://admin.tkcat.cn/apider/getBeUpdatedList?code=ekd503738k'
BASE_GET_COUPONS_HOST = 'http://admin.tkcat.cn/apider/getBeUpdatedList?code=ekd503738k'

BASE_GET_COUPONS_UPDATE_HOST = 'http://admin.tkcat.cn/apider/getCouponList?code=ekd503738k'
BASE_UPLOAD_COUPONS_UPDATE_HOST = 'http://admin.tkcat.cn/apider/updateCouponList?code=ekd503738k'
# BASE_GET_COUPONS_UPDATE_HOST = 'http://10.4.250.198:8080/apider/getCouponList?code=ekd503738k'
# BASE_UPLOAD_COUPONS_UPDATE_HOST = 'http://10.4.250.198:8080/apider/updateCouponList?code=ekd503738k'

BASE_GET_ITEM_PRICE_UPDATE_HOST = 'http://admin.tkcat.cn/apider/getFeedbackGoodsList?code=ekd503738k'
BASE_UPLOAD_ITEM_PRICE_UPDATE_HOST = 'http://admin.tkcat.cn/apider/saveReplacePrice?code=ekd503738k'

BASE_GET_EXISTING_COMMODITY_HOST = 'http://pc.jd.tkcat.cn/pc/goods/open/list.json?token=2DC071D4AE444EEDAE7C68&page='

BASE_COOKIE_FILE = 'cookies/jd_cookies.txt'
BASE_MJD_COOKIE_FILE = 'cookies/mjd_cookies.txt'

BASE_CSV_FILE = 'csv/csv_items.csv'
BASE_CSV_UNIQ_FILE = 'csv/csv_uniq_items.csv'
BASE_SKUID_CSV_FILE = 'csv/csv_skuid_items.csv'
BASE_SKUID_CSV_UNIQ_FILE = 'csv/csv_uniq_skuid_items.csv'
BASE_COUPONS_CSV_FILE = 'csv/csv_coupons.csv'
BASE_COUPONS_CSV_UNIQ_FILE = 'csv/csv_uniq_coupons.csv'
BASE_ITEMS_EXP_CSV_FILE = 'csv/csv_items_exp.csv'
BASE_ITEMS_EXP_CSV_UNIQ_FILE = 'csv/csv_uniq_items_exp.csv'
BASE_ITEMS_EXP_ID_CSV_UNIQ_FILE = 'csv/csv_uniq_items_exp_id.csv'
BASE_EXISTING_SKUID_UNIQ_FILE = 'csv/csv_uniq_existing_skuids.csv'
BASE_EXISTING_COUPONS_UNIQ_FILE = 'csv/csv_uniq_existing_coupons.csv'
BASE_EXISTING_COMPOUND_UNIQ_FILE = 'csv/csv_uniq_existing_compound.csv'

BASE_CSV_LIMIT = 10000
BASE_MAX_PAGE = 10
SLEEP_TIMEPAGE_DONE = 0.3
SLEEP_TIMEPAGE_ERR = 0.2
TIMEOUT_DOOGS_PAGE_CONNECT = 4.0
TIMEOUT_DOOGS_PAGE_REQUEST = 6.0
TIMEOUT_UPLOAD_CONNECT = 60.0
TIMEOUT_UPLOAD_REQUEST = 300.0
LOGIN_SLEEP_TIME = 5.0

MJD_LOGIN_NAME = '17314821730'
MJD_LOGIN_PASSWORD = 'net@jixunsoft.cn'
