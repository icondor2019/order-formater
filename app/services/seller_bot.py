from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from repositories.catalogue_repository import CatalogueRepository
from repositories.seller_repository import SellerRepository
from repositories.product_repository import ProductRepository
from responses.seller_response import SellerResponse
from data_models.sellerEnum import SellerStatusEnum
from utils.llm_matcher_tool import LlmMatcher
from configuration.settings import settings
from telegram import Update
from loguru import logger
from uuid import uuid4


class TelegramBot:
    def __init__(self):
        self.telegram_token = settings.TELEGRAM_BOT_TOKEN
        self.telegram_user = settings.TELEGRAM_BOT_USER
        self.__seller_repository = SellerRepository()
        self.__catalogue_repository = CatalogueRepository()
        self.__product_repository = ProductRepository()

    async def new_seller(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        logger.debug(f"New register request. User ID: {user_id}")
        seller_register = self.__seller_repository.get_seller_record(str(user_id))

        if seller_register:
            await update.message.reply_text("""You have registered already. \nPlease select another option from the menu.
                                            \nIf you what to update your offer, just send your dispo. We will proccessed for you.""")
        else:
            seller_response = SellerResponse(uuid=str(uuid4()),
                                             user_id=str(user_id))
            self.__seller_repository.create_seller(seller_response)
            await update.message.reply_text('Welcome, please enter your company name. \nThis is the name customer will see.')

    async def current_offer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        seller_register = self.__seller_repository.get_seller_record(str(user_id))
        dispo = self.__product_repository.get_all_active_seller_products(seller_uuid=seller_register.uuid)
        base_txt = f"{seller_register.name} has {len(dispo)} active products\n\n"
        dispo_txt = "\n".join([f"{row[1]} {row[0]}, price: {row[2]:.2f}" for row in dispo])
        response_txt = base_txt + dispo_txt
        await update.message.reply_text(response_txt)

    async def delete_offer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        logger.debug(f"User ID: {user_id}")
        seller_register = self.__seller_repository.get_seller_record(str(user_id))
        self.__product_repository.deactivate_seller_products(seller_uuid=seller_register.uuid)
        await update.message.reply_text('seller offer_deleted')

    def handle_response(self, text: str, context: ContextTypes.DEFAULT_TYPE, update: Update):
        # processed_text = text.lower()
        msg = "Hello, please select one of the available option in the menu:\
            \n/new_seller : If your are new, we will register your company in our database\
            \n/current_offer : Check your current dispo\
            \n/delete_offer : We'll delete your current dispo"
        return msg

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.debug('Enter handle_message...')
        user_id = update.message.from_user.id
        logger.debug(f"User ID: {user_id}")
        seller_register = self.__seller_repository.get_seller_record(str(user_id))
        msg_text = update.message.text
        logger.debug(msg_text)

        if seller_register:
            seller_uuid = seller_register.uuid
            if seller_register.status == SellerStatusEnum.pending:
                seller_register.status = SellerStatusEnum.active.value
                seller_register.name = msg_text
                logger.debug(seller_register)

                self.__seller_repository.update_seller_data(seller_register)
                await update.message.reply_text(f"""Thank you, your company {msg_text} is registered.
                                                \nYou can pick any option from our menu to do several actions.""")
                return
            elif seller_register.status == SellerStatusEnum.active:
                logger.info('processing offer...')
                len_offer = LlmMatcher().process_raw_availability(seller_uuid=seller_uuid, raw_text=msg_text)
                await update.message.reply_text(f'Thank you. We are updating your offer in our system. Total products: {len_offer}')
                return

        message_type = update.message.chat.type
        msg_text = update.message.text
        if message_type == 'group':
            if msg_text.startswith(self.telegram_user):
                new_text = msg_text.replace(self.telegram_user, '')
                response = self.handle_response(new_text, context, update)
            else:
                return
        else:
            response = self.handle_response(msg_text, context, update)
        await update.message.reply_text(response)

    async def error_msg(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Update {update} caused error {context.error}")
        await update.message.reply_text('Ha ocurrido un error...')

    def update_seller_availability(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        logger.debug(f"User ID: {user_id} is updating availability.")

    def run(self):
        logger.info('init bot...')
        app = Application.builder().token(self.telegram_token).build()
        app.add_handler(CommandHandler('new_seller', self.new_seller))
        app.add_handler(CommandHandler('current_offer', self.current_offer))
        app.add_handler(CommandHandler('delete_offer', self.delete_offer))
        app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        app.add_error_handler(self.error_msg)
        logger.info('bot running...')
        app.run_polling(poll_interval=5, timeout=10)
