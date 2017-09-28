import os


class Auditor:
    def __init__(self, file_path='html_files/pr_metadata.txt'):
        self.page_record = {}
        self.count_error_code = 0
        self.count_200 = 0
        self.crawl_record = {}
        self.start_time = 0
        self.end_time = 0
        self.count_robot_excluded = 0
        self.site_limit = {}
        self.file_path = file_path

    def write_summary(self):
        for count in self.crawl_record:
            self.crawl_record[count].final_page_rank = self.page_record[self.crawl_record[count].url].page_rank
        total_size = 0
        for dirpath, dirnames, filenames in os.walk("html_files"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        f = open(self.file_path, "a")
        f.write("==================================== Page Rank Summary====================================")
        f.write("\nTotal page crawled:" + str(len(self.crawl_record)))
        f.write("\nTotal pages:" + str(len(self.page_record)))
        f.write("\nTotal size:" + str(total_size) + " bytes")
        f.write("\nStart Time:" + str(self.start_time))
        f.write("\nEnd Time:" + str(self.end_time))
        f.write("\nTime take:" + str(self.end_time - self.start_time))
        f.write("\nTotal success 200:" + str(self.count_200))
        f.write("\nTotal failed:" + str(self.count_error_code))
        f.write("\nTotal robot exclude:" + str(self.count_robot_excluded))
        f.write("\n==================================== Page Rank Detail====================================")
        for record in self.crawl_record:
            f.write("\n\nNo:" + str(self.crawl_record[record].num)
                    + " Url -> " + self.crawl_record[record].url
                    + " time: " + str(self.crawl_record[record].time)
                    + " code: " + str(self.crawl_record[record].code)
                    + "\nPage Rank: " + str(self.crawl_record[record].page_rank)
                    + "\nFinal Page Rank: " + str(self.crawl_record[record].final_page_rank))
        f.write("\n==================================== Sites Detail====================================")
        for site in self.site_limit:
            f.write("\nSite: " + site + " Num: " + str(self.site_limit[site]))
        f.close()

