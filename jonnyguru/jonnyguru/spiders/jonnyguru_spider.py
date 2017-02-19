# -*- coding: utf-8 -*-
import re

import scrapy


class JonnyguruSpider(scrapy.Spider):
    name = "jonnyguru"
    allowed_domains = ["jonnyguru.com"]
    # Starts at PSU Reviews
    start_urls = ['http://www.jonnyguru.com/modules.php?name=NDReviews&op=Review_Cat&recatnum=13']

    # Common XPaths
    scoring_href_xpath = '//select/option[contains(., "Page ")]/@value'
    summary_table_xpath = '//*[contains(text(), "Total Score")]/ancestor::table[position() = 1]//tr//text()'

    def parse(self, response):
        """Finds links to PSU Reviews"""
        # TODO make sure we don't depend on get params order
        psu_review_href = '//a[starts-with(@href, "modules.php?name=NDReviews&op=Story&reid=")]/@href'
        review_paging_href = '//a[starts-with(@href, "modules.php?name=NDReviews&op=Review_Cat&recatnum=13&pagenum=")]/@href'

        next_pages = response.xpath(psu_review_href).extract()
        review_paging_pages = response.xpath(review_paging_href).extract()

        for next_page in next_pages:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse_review_summary_link)

        for next_page in review_paging_pages:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_review_summary_link(self, response):
        # Might be that the first page of review already contains the summary table.
        # The extracted link would be identical and deduped, thus, we have to parse the resulting score here.
        summary_table = response.xpath(JonnyguruSpider.summary_table_xpath).extract()

        if summary_table:
            # The first PSU Review page already has a scoring table
            summary_dict = JonnyguruSpider.parse_review_summary_score(response)
            yield next(summary_dict)

        # We select the last "Page X" from the "menu", which is the Scoring/Summary page
        scoring_href = response.xpath(JonnyguruSpider.scoring_href_xpath)[-1].extract()
        scoring_href = response.urljoin(scoring_href)
        yield scrapy.Request(scoring_href, callback=self.parse_review_summary_score)

    @staticmethod
    def parse_review_summary_score(response):
        # List of all possible attributes ever
        psu_review = {
            'name': JonnyguruSpider.extract_psu_name(response),
        }
        # Extracts every text node in the whole Summary Table,
        # this way we don't have to care about various tag combinations
        summary_table = response.xpath(JonnyguruSpider.summary_table_xpath).extract()
        psu_review['scores'] = JonnyguruSpider.parse_summary_table(summary_table)

        yield psu_review

    @staticmethod
    def parse_summary_table(summary_table):
        # Strips irrelevant text nodes
        stripped_summary_table = list(filter(bool, [node.strip() for node in summary_table]))
        # The cleaned table looks like: [attr1, score1, attr2, score2, ..., total_attr, total_score]
        attrs = stripped_summary_table[::2]
        vals = stripped_summary_table[1::2]
        return dict(zip(attrs, vals))

    @staticmethod
    def normalize_psu_name(psu_name):
        return re.sub(r'^Reviews - ', '', psu_name)

    @staticmethod
    def extract_psu_name(response):
        """PSU Name is in the first td.row-header"""
        psu_name = response.xpath('//td[@class = "row-header"]//text()').extract_first()
        return JonnyguruSpider.normalize_psu_name(psu_name)

