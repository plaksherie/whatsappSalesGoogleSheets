import gspread


class BaseSheet:
    def __init__(
            self,
            url_sheet: str,
            name_work_sheet: str,
            service_file: str = 'service_account.json'
    ) -> None:
        self.gc = gspread.service_account(service_file)
        self.sheet = self.gc.open_by_url(url_sheet)
        self.worksheet = self.sheet.worksheet(name_work_sheet)
