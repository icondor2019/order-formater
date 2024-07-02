from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from repositories.catalogue_repository import CatalogueRepository
from repositories.seller_repository import SellerRepository
from responses.seller_response import SellerResponse
from data_models.sellerEnum import SellerStatusEnum
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


    async def new_seller(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        logger.debug(f"New register request. User ID: {user_id}")
        seller_register = self.__seller_repository.get_seller_record(str(user_id))

        if seller_register:
            await update.message.reply_text('You have registered already. \nPlease select another option from the menu\
                                            If you what to update your offer, just send your dispo. We will proccessed for you.')
        else:
            seller_response = SellerResponse(uuid=str(uuid4()),
                                             user_id=str(user_id))
            self.__seller_repository.create_seller(seller_response)
            await update.message.reply_text('Welcome, please enter your company name. \nThis is the name customer will see.')

    async def current_offer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # TODO service to consult in db current offer
        await update.message.reply_text('offer_updated...')

    async def delete_offer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # TODO service to delete current offer
        await update.message.reply_text('seller offer_deleted')

    def handle_response(self, text: str, context: ContextTypes.DEFAULT_TYPE, update: Update):
        processed_text = text.lower()
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
        text = update.message.text

        if seller_register:
            if seller_register.status == SellerStatusEnum.pending:
                seller_register.status = SellerStatusEnum.active.value
                seller_register.name = text
                logger.debug(seller_register)

                self.__seller_repository.update_seller_data(seller_register)
                await update.message.reply_text(f'Thank you, your company {text} is registered.\nPlease send your dispo...')
                return
            elif seller_register.status == SellerStatusEnum.active:
                logger.info('processing offer...')
                # TODO  service to process new offers & match products
                await update.message.reply_text(f'Thank you. We are updating your offer in our system. Total products: 8')
                return

        message_type = update.message.chat.type
        text = update.message.text
        if message_type == 'group':
            if text.startswith(self.telegram_user):
                new_text = text.replace(self.telegram_user, '')
                response = self.handle_response(new_text, context, update)
            else:
                return    
        else:
            response = self.handle_response(text, context, update)
        await update.message.reply_text(response)

    async def error_msg(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Update {update} caused error {context.error}")
        await update.message.reply_text('Ha ocurrido un error...')

    def created_new_seller(self, telegram_seller_id, seller_name):
        seller_uuid = str(uuid4())
        logger.debug(seller_uuid)
        # TODO save seller uuid in db
        return seller_uuid

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
