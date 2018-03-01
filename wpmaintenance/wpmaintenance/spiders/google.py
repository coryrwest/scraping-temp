# -*- coding: utf-8 -*-
import scrapy, re, requests, json, logging
from scrapy.loader import ItemLoader
from wpmaintenance.items import WpmaintenanceItem
from scrapy import signals, Spider
from urlparse import urlparse

logging.getLogger("requests").setLevel(logging.WARNING)

class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['google.com']
    #start_urls = ['https://www.google.com/search?source=hp&q=pet+grooming+92592&oq=pet+grooming+92592']
    
    zipcodes = ['92592']#, '90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90010', '90011', '90012', '90013', '90014', '90015', 
    #'90016', '90017', '90018', '90019', '90020', '90021', '90022', '90023', '90024', '90025', '90026', '90027', '90028', '90029', '90031', '90032', '90033', 
    #'90034', '90035', '90036', '90037', '90038', '90039', '90040', '90041', '90042', '90043', '90044', '90045', '90046', '90047', '90048', '90049', '90056', 
    #'90057', '90058', '90059', '90061', '90062', '90063', '90064', '90065', '90066', '90067', '90068', '90069', '90071', '90077', '90201', '90210', '90211', 
    #'90212', '90220', '90221', '90222', '90230', '90232', '90240', '90241', '90242', '90245', '90247', '90248', '90249', '90250', '90254', '90255', '90260', 
    #'90261', '90262', '90263', '90265', '90266', '90270', '90272', '90274', '90275', '90277', '90278', '90280', '90290', '90291', '90292', '90293', '90301', 
    #'90302', '90303', '90304', '90305', '90401', '90402', '90403', '90404', '90405', '90501', '90502', '90503', '90504', '90505', '90601', '90602', '90603', 
    #'90604', '90605', '90606', '90620', '90621', '90623', '90630', '90631', '90638', '90640', '90650', '90660', '90670', '90680', '90701', '90703', '90704', 
    #'90706', '90710', '90712', '90713', '90715', '90716', '90717', '90720', '90723', '90731', '90732', '90740', '90742', '90743', '90744', '90745', '90746', 
    #'90747', '90755', '90802', '90803', '90804', '90805', '90806', '90807', '90808', '90810', '90813', '90814', '90815', '90822', '91001', '91006', '91007', 
    #'91010', '91011', '91016', '91020', '91024', '91030', '91040', '91042', '91101', '91103', '91104', '91105', '91106', '91107', '91108', '91201', '91202', 
    #'91203', '91204', '91205', '91206', '91207', '91208', '91214', '91301', '91302', '91303', '91304', '91306', '91307', '91311', '91316', '91320', '91321', 
    #'91324', '91325', '91326', '91331', '91335', '91340', '91342', '91343', '91344', '91345', '91350', '91351', '91352', '91354', '91355', '91356', '91360', 
    #'91361', '91362', '91364', '91367', '91377', '91381', '91384', '91401', '91402', '91403', '91405', '91406', '91411', '91423', '91436', '91501', '91502', 
    #'91504', '91505', '91506', '91601', '91602', '91604', '91605', '91606', '91607', '91608', '91701', '91702', '91706', '91709', '91710', '91711', '91722', 
    #'91723', '91724', '91730', '91731', '91732', '91733', '91737', '91739', '91740', '91741', '91743', '91744', '91745', '91746', '91748', '91750', '91752', 
    #'91754', '91755', '91759', '91761', '91762', '91763', '91764', '91765', '91766', '91767', '91768', '91770', '91773', '91775', '91776', '91780', '91784', 
    #'91786', '91789', '91790', '91791', '91792', '91801', '91803', '91901', '91902', '91905', '91906', '91910', '91911', '91913', '91914', '91915', '91916', 
    #'91917', '91931', '91932', '91934', '91935', '91941', '91942', '91945', '91948', '91950', '91962', '91963', '91977', '91978', '91980', '92003', '92004', 
    #'92007', '92008', '92009', '92014', '92019', '92020', '92021', '92024', '92025', '92026', '92027', '92028', '92029', '92036', '92037', '92040', '92054', 
    #'92056', '92057', '92059', '92060', '92061', '92064', '92065', '92066', '92067', '92069', '92070', '92071', '92075', '92078', '92082', '92083', '92084', 
    #'92086', '92091', '92101', '92102', '92103', '92104', '92105', '92106', '92107', '92108', '92109', '92110', '92111', '92113', '92114', '92115', '92116', 
    #'92117', '92118', '92119', '92120', '92121', '92122', '92123', '92124', '92126', '92127', '92128', '92129', '92130', '92131', '92139', '92154', '92173', 
    #'92201', '92203', '92210', '92211', '92220', '92223', '92225', '92227', '92230', '92231', '92233', '92234', '92236', '92239', '92240', '92241', '92242', 
    #'92243', '92249', '92250', '92251', '92252', '92253', '92254', '92256', '92257', '92258', '92259', '92260', '92262', '92264', '92266', '92267', '92268', 
    #'92270', '92273', '92274', '92275', '92276', '92277', '92280', '92281', '92282', '92283', '92284', '92285', '92301', '92304', '92305', '92307', '92308', 
    #'92309', '92310', '92311', '92313', '92314', '92315', '92316', '92317', '92318', '92320', '92321', '92323', '92324', '92325', '92327', '92332', '92333', 
    #'92335', '92336', '92337', '92339', '92341', '92342', '92345', '92346', '92347', '92352', '92354', '92356', '92358', '92359', '92363', '92364', '92365', 
    #'92368', '92371', '92372', '92373', '92374', '92376', '92377', '92382', '92386', '92392', '92394', '92397', '92398', '92399', '92401', '92404', '92405', 
    #'92407', '92408', '92410', '92411', '92501', '92503', '92504', '92505', '92506', '92507', '92508', '92509', '92518', '92530', '92532', '92536', '92539', 
    #'92543', '92544', '92545', '92548', '92549', '92551', '92553', '92555', '92557', '92561', '92562', '92563', '92567', '92570', '92571', '92582', '92583', 
    #'92584', '92585', '92586', '92587', '92590', '92591', '92592', '92595', '92596', '92602', '92604', '92606', '92610', '92612', '92614', '92618', '92620', 
    #'92624', '92625', '92626', '92627', '92629', '92630', '92646', '92647', '92648', '92649', '92651', '92653', '92655', '92656', '92657', '92660', '92661', 
    #'92662', '92663', '92672', '92673', '92675', '92676', '92677', '92679', '92683', '92688', '92691', '92692', '92694', '92701', '92703', '92704', '92705', 
    #'92706', '92707', '92708', '92780', '92782', '92801', '92802', '92804', '92805', '92806', '92807', '92808', '92821', '92823', '92831', '92832', '92833', 
    #'92835', '92840', '92841', '92843', '92844', '92845', '92860', '92861', '92865', '92866', '92867', '92868', '92869', '92870', '92879', '92880', '92881', 
    #'92882', '92883', '92886', '92887', '93001', '93003', '93004', '93010', '93012', '93015', '93021', '93022', '93023', '93030', '93033', '93035', '93040', 
    #'93041', '93060', '93063', '93065', '93066', '93252', '93510', '93532', '93534', '93535', '93536', '93543', '93544', '93550', '93551', '93552', '93553', 
    #'93562', '93563', '93591']
    
    industries = [
        # 'pet store',
        # 'auto parts',
        # 'food store',
        # 'restaurant',
        # 'pizza',
        # 'clothing store',
        # 'ice cream',
        'auto repair',
        # 'car wash',
        # 'computer repair',
        # 'electronics repair',
        # 'personal trainer',
        # 'coffee shop',
        # 'bar',
        'pet grooming',
        'pet boarding',
        'vape shop',
        # 'bakery',
        'landscaping',
        'tutor',
        'daycare',
        # 'haircut',
        'cleaning',
        # 'bookstore',
        # 'flower shop',
        'massage',
        'micro brewery'
    ]
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GoogleSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
        
    def spider_closed(self, spider):
        spider.crawler.stats.get_stats()
    
    def start_requests(self):
        #https://serpcloud.com/packages
        #http://serpmetrics.com/docs/signup
        #http://www.serpprovider.com/
        #https://serps.com/trial-signup/
        #https://serpapi.com/search?q=Pet+grooming+92592&num=100&output=json&api_key=demo
        for industry in self.industries:
            zipcode = self.zipcodes[0]
            part = (industry + ' ' + zipcode).replace(" ", "+")
            href = 'https://serpapi.com/search?q=' + str(part) + '&num=100&output=json&api_key=demo'
            self.logger.info('Starting %s', href)
            r = requests.get(href, timeout=20)
            parsed_json = r.json()
            results = parsed_json['organic_results']
            for result in results:
                request = scrapy.Request(result['link'], callback=self.parse)
                request.meta['industry'] = industry
                request.meta['zipcode'] = zipcode
                yield request
        
    def parse(self, response):
        wpsite = WpmaintenanceItem()
        
        url = urlparse(response.url)
        hostname = url.scheme + '://' + url.netloc
        #self.logger.info('Checking %s', hostname)
        
        if 'wp-content' in response.text or 'wp-includes' in response.text:
            wpsite["industry"] = response.meta['industry']
            wpsite["zipcode"] = response.meta['zipcode']
            wpsite['url'] = response.url
            wpsite['found_by_check'] = 'wp-content'
            self.logger.info('Found a wordpress site by wp-content: %s', response.url)
            yield wpsite
        else:
            r = requests.get(hostname + '/license.txt', verify=False, timeout=20, allow_redirects=False)
            if r.status_code == 200 and 'WordPress' in r.content:
                wpsite["industry"] = response.meta['industry']
                wpsite["zipcode"] = response.meta['zipcode']
                wpsite['url'] = response.url
                wpsite['found_by_check'] = 'license'
                self.logger.info('Found a wordpress site by license: %s', response.url)
                yield wpsite
            else:
                r = requests.get(hostname + '/readme.html', verify=False, timeout=20, allow_redirects=False)
                if r.status_code == 200 and 'WordPress' in r.content:
                    wpsite["industry"] = response.meta['industry']
                    wpsite["zipcode"] = response.meta['zipcode']
                    wpsite['url'] = response.url
                    wpsite['found_by_check'] = 'readme'
                    self.logger.info('Found a wordpress site by readme: %s', response.url)
                    yield wpsite
                else:
                    r = requests.get(hostname + '/wp-trackback.php', verify=False, timeout=20, allow_redirects=False)
                    if r.status_code == 200:
                        wpsite["industry"] = response.meta['industry']
                        wpsite["zipcode"] = response.meta['zipcode']
                        wpsite['url'] = response.url
                        wpsite['found_by_check'] = 'wp-trackback'
                        self.logger.info('Found a wordpress site by wp-trackback: %s', response.url)
                        yield wpsite
                    else:
                        r = requests.get(hostname + '/wp-login.php', verify=False, timeout=20, allow_redirects=False)
                        if r.status_code == 200:
                            wpsite["industry"] = response.meta['industry']
                            wpsite["zipcode"] = response.meta['zipcode']
                            wpsite['url'] = response.url
                            wpsite['found_by_check'] = 'wp-login'
                            self.logger.info('Found a wordpress site by wp-login: %s', response.url)
                            yield wpsite
        return
        
    # def parse(self, response):
    #     # if we are on the last page, do nothing.
    #     if 'start=100' in response.url:
    #         self.logger.info('Reached end of search results, exiting...')
    #         return
    #     # If we have a google results page, run the google stuff.
    #     if 'google' in response.url:
    #         # go through the first 5 pages of google results and get the urls for those sites.
    #         links = response.selector.css('#ires a')
    #         sites = []    
    #         if links is None:
    #             self.logger.error('PAGE WAS NOT WHAT WAS EXPECTED')
    #         else:
    #             for link in links:
    #                 href = link.css('::attr("href")').extract_first()
    #                 if 'google' not in href:
    #                     sites.append(href)
    #         # navigate to the next page
    #         if '&start=' not in response.url:
    #             yield scrapy.Request(response.url + '&start=10', callback=self.parse)
    #         else:
    #             start = re.search('start\=[0-9]+', response.url)
    #             # split to get the number
    #             num = int(start.group(0).split('=')[1])
    #             yield scrapy.Request(response.url + '&start=' (num + 10), callback=self.parse)
    #     # otherwise check for WP
    #     else:
    #         return
    #     #https://www.google.com/search?q=pet+grooming+92592&start=10
    #     return
