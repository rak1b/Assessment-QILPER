from coreapp.helper import *
from inventory.models import *
from coreapp.models import Document, User
from web_settings.models import *
from restaurant.models import *
from restaurant.api.admin.serializers import ClientSerializer
from web_settings.models import Business_category
class BulkImportUtils:
    def set_file_path(self, filepath):
        self.csv_filepath = "media/"+filepath+"/csv/"
        self.img_filepath = filepath+"/images/"

    def create_document(self, image):
        document = Document.objects.create(document=image, owner=self.request.user, doc_type=0)
        return document

    def bulk_import(self, uploaded_file_path):
        pass

    def get_file_name(self, prefix="Product"):
        return prefix+str(uuid.uuid4())+datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.xlsx'

    def upload_file(self, file, file_path,prefix="Product"):
        self.set_file_path(file_path)
        fs = FileSystemStorage(location=self.csv_filepath)
        content = file.read()
        file_content = ContentFile(content)
        file_name = fs.save(self.get_file_name(prefix=prefix), file_content)
        uploaded_file_path = fs.path(file_name)
        return uploaded_file_path


class ProductBulkImport(BulkImportUtils):
    images = []
    result = []
    heading = []
    client = None

    def get_or_create_parent_category(self, category):
        category_obj = Category.objects.filter(name=category).first()
        if category_obj:
            return category_obj
        else:
            category_obj = Category.objects.create(name=category, parent=None)
            return category_obj

    def get_or_create_category(self, category, parent_category,client):
        if parent_category is not None :
            parent = self.get_or_create_parent_category(parent_category)
        else:
            parent = None
        category_obj = Category.objects.filter(name=category,branches=client).first()
        if category_obj:
            return category_obj
        else:
            category_obj = Category.objects.create(name=category, parent=parent)
            client = Client.objects.get(id=client)
            category_obj.branches.add(client)
            category_obj.save()
            return category_obj

    def create_product(self, name, category,parent_category, regular_price,sale_price, description, image, is_today_special,vat_type):
        category = self.get_or_create_category(category, parent_category,self.client)
        product_obj = Product.objects.create(name=name, client_id=self.client, is_today_special=is_today_special,vat_type=vat_type,
                                             category=category, regular_price=regular_price, sale_price=sale_price, desc=description, thumb=image)
        return product_obj

    def create_objects(self, result):
        index = 0
        for item in self.result:
            if item['name'] == 'name':  # skip heading
                continue
            image = self.create_document(self.images[index])
            row = item['row']
            column = item['column']
            name = item['name']
            category = item['category']
            parent_category = item['parent_category']
            regular_price = item['regular_price']
            sale_price = item['sale_price']
            description = item['description']
            vat_type = item['vat_type']
            is_today_special = True if item['is_today_special'] == str(1) else False
            row_column_text = f"Row : {row} Product : {name}"
            product = self.create_product(name, category,parent_category, regular_price,sale_price, description, image, is_today_special,vat_type)
            index += 1
        

    def bulk_import(self, file, filepath, request, client):
        self.user = request.user
        self.client = client
        uploaded_file_path = self.upload_file(file, filepath)
        wb = load_workbook(uploaded_file_path)
        sheet = wb["Sheet1"]
        max_column = sheet.max_column
        max_row = sheet.max_row
        self.result = []

        for row in range(1, max_row+1):
            current_data = {}
            new_path = ''
            for column in range(1, max_column+1):
                value = sheet.cell(row, column).value
                if row == 1:
                    self.heading.append(value)

                if column == 2 and row != 0:
                    try:
                        # if row!=max_row
                        image_loader = SheetImageLoader(sheet)
                        image = image_loader.get('B' + str(row+1))
                        dir_path = self.img_filepath
                        pathlib.Path(settings.MEDIA_ROOT + f"/{dir_path}").mkdir(parents=True, exist_ok=True)
                        new_path = dir_path + f"{uuid.uuid4()}.PNG"
                        if image:
                            image.save(settings.MEDIA_ROOT + f"/{new_path}", "PNG", optimize=False, quality=100)
                        self.images.append(new_path)

                    except Exception as e:
                        print("error for no image ", e)
                        default_path =  "/default/products/default.png"
                        self.images.append(default_path)
                        
                else:
                    try:
                        current_data[self.heading[column-1]] = value
                        current_data["row"] = row
                        current_data["column"] = column
                    except:
                        traceback.print_exc()
            self.result.append(current_data)
        self.create_objects(self.result)
        print("images", self.images)
        return 1



class ClientBulkImport(BulkImportUtils):
    images = []
    covers = []
    result = []
    heading = []

    def create_or_get_company_category(self, category):
        company_category = Business_category.objects.filter(name=category).first()
        if company_category:
            return company_category.id
        else:
            company_category = Business_category.objects.create(name=category)
            return company_category.id
    def get_billing_type(self, billing_type):
        return  Billing_type.objects.filter(name=billing_type).first().id
     
    def create_objects(self):
        index = 0
        for item in self.result:
            if item['company_name'] == 'company_name':  # skip heading
                continue
            image = self.create_document(self.images[index])
            cover = self.create_document(self.covers[index])
            item['logo'] = image.id
            item['cover'] = [cover.id]
            item['company_service_type'] = int(item['company_service_type'])
            print("item['restaurant_types']", item['restaurant_types'])
            try:
                item['restaurant_types'] = item['restaurant_types'].split(',')
            except:
                pass
            item['company_category'] = self.create_or_get_company_category(item['company_category'])
            # item['payment_billing_type'] = self.get_billing_type(item['payment_billing_type'])
            item['status'] = int(item['status'])
            item['menu'] = []
            item['gallery'] = []
            item['branch'] = []

            serializer = ClientSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            import logging
            logger = logging.getLogger('django')
            logger.error(f'-----------item------------------: {index}')
            logger.error(f"creating client : { item['company_name']} ")

            index+=1
    
    def add_and_save_images(self,sheet,row,column_letter="B"):
        image_loader = SheetImageLoader(sheet)
        image = image_loader.get(column_letter + str(row+1))
        dir_path = self.img_filepath
        pathlib.Path(settings.MEDIA_ROOT + f"/{dir_path}").mkdir(parents=True, exist_ok=True)
        new_path = dir_path + f"{uuid.uuid4()}.PNG"
        if image:
            image.save(settings.MEDIA_ROOT + f"/{new_path}", "PNG", optimize=False, quality=100)
        return new_path

    def bulk_import(self, file, filepath, request, client=None):
        self.user = request.user
        self.client = client
        uploaded_file_path = self.upload_file(file, filepath,prefix="client")
        wb = load_workbook(uploaded_file_path)
        sheet = wb["Sheet1"]
        max_column = sheet.max_column
        max_row = sheet.max_row
        self.result = []

        for row in range(1, max_row+1):
            print("row", row)
            current_data = {}
            new_path = ''
            for column in range(1, max_column+1):
                value = sheet.cell(row, column).value
                if row == 1:
                    self.heading.append(value)

                if column == 2 and row != 0:
                    try:
                        # if row!=max_row
                        image_loader = SheetImageLoader(sheet)
                        image = image_loader.get('B' + str(row+1))
                        dir_path = self.img_filepath
                        pathlib.Path(settings.MEDIA_ROOT + f"/{dir_path}").mkdir(parents=True, exist_ok=True)
                        new_path = dir_path + f"{uuid.uuid4()}.PNG"
                        if image:
                            image.save(settings.MEDIA_ROOT + f"/{new_path}", "PNG", optimize=False, quality=100)
                        self.images.append(new_path)

                    except Exception as e:
                        print("error ", e)
                        pass
                if column == 3 and row != 0:
                    try:
                        # if row!=max_row
                        image_loader = SheetImageLoader(sheet)
                        image = image_loader.get('C' + str(row+1))
                        dir_path = self.img_filepath
                        pathlib.Path(settings.MEDIA_ROOT + f"/{dir_path}").mkdir(parents=True, exist_ok=True)
                        new_path = dir_path + f"{uuid.uuid4()}.PNG"
                        if image:
                            image.save(settings.MEDIA_ROOT + f"/{new_path}", "PNG", optimize=False, quality=100)
                        self.covers.append(new_path)

                    except Exception as e:
                        print("error ", e)
                        pass
                else:
                    try:
                        current_data[self.heading[column-1]] = value
                        current_data["row"] = row
                        current_data["column"] = column
                    except:
                        traceback.print_exc()
            self.result.append(current_data)
        # for item in self.result:
        #     print(item)
        #     print()
        #     print()


        #     import logging
        #     logger = logging.getLogger('django')
            
        #     logger.error(f'-----------item------------------')
        #     logger.error(f'{item}')
        # print(self.images)
        # print()

        # print(self.covers)
        print('result ', self.result)
        self.create_objects()
        return 1


