from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from test_runner import run_test
import os.path

def start(update, context):
    context.user_data['year'] = None
    context.user_data['p_party'] = None
    context.user_data['threshold_idx'] = None
    update.message.reply_text('Olá! Informe o ano a considerar (de 2002 a 2023):')
    return 1

def question1(update, context):
    context.user_data['year'] = update.message.text
    update.message.reply_text('Ótimo! Agora, informe os partidos a analisar, separados por espaço (ex. PT MDB PL), envie ALL caso queira todos:')
    return 2

def question2(update, context):
    context.user_data['p_party'] = update.message.text
    update.message.reply_text('Ok! Por fim, informe o percentual mínimo de concordância (threshold) - entre 0 e 1 (ex. 0.9):')
    return 3

def question3(update, context):
    try:
        context.user_data['threshold_idx'] = float(update.message.text)
    except ValueError:
        update.message.reply_text('Valor inválido. Por favor, digite um valor entre 0 e 1.')
        return 3
    update.message.reply_text('Aguarde um momento, estamos gerando os gráficos...')
    if context.user_data['p_party'] == 'ALL':
        if not path_checker(context):
            run_test(context.user_data['year'], '', context.user_data['threshold_idx'])
    else:
        if not path_checker(context):
            run_test(context.user_data['year'], context.user_data['p_party'], context.user_data['threshold_idx'])
    update.message.reply_text('Graficos gerados com sucesso, digite qualquer coisa para visualizar')
    return 4

def path_checker(context):
    year = context.user_data['year']
    p_party = context.user_data['p_party']
    threshold_idx = context.user_data['threshold_idx']

    p_party = p_party.replace(' ','_')
    betwenness_path = '/'.join(['betwenness_', f'betwenness_{year}_{p_party}_{threshold_idx}.png'])
    heatmap_path = '/'.join(['heatmap_', f'heatmap_{year}_{p_party}_{threshold_idx}.png'])
    graph_path = '/'.join(['graph_', f'graph_{year}_{p_party}_{threshold_idx}.png'])
     
    if os.path.exists(betwenness_path) and os.path.exists(heatmap_path) and os.path.exists(graph_path):
        return True

def view(update, context):
    year = context.user_data['year']
    p_party = context.user_data['p_party']
    threshold_idx = context.user_data['threshold_idx']
    
    p_party = p_party.replace(' ','_')
    betwenness_path = '/'.join(['betwenness_', f'betwenness_{year}_{p_party}_{threshold_idx}.png'])
    heatmap_path = '/'.join(['heatmap_', f'heatmap_{year}_{p_party}_{threshold_idx}.png'])
    graph_path = '/'.join(['graph_', f'graph_{year}_{p_party}_{threshold_idx}.png'])
    
    try:
        update.message.reply_text("Betwenness:")
        with open(betwenness_path, 'rb') as f:
            update.message.reply_photo(f)
        update.message.reply_text("Heatmap:")
        with open(heatmap_path, 'rb') as f:
            update.message.reply_photo(f)
        update.message.reply_text("Graph:")
        with open(graph_path, 'rb') as f:
            update.message.reply_photo(f)
        update.message.reply_text("/start caso queira reiniciar o programa")
        return ConversationHandler.END
    
    except Exception:
        update.message.reply_text('Erro ao gerar os dados. Por favor, tente novamente. /start')
        return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('A conversa foi cancelada.')
    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, question1)],
            2: [MessageHandler(Filters.text & ~Filters.command, question2)],
            3: [MessageHandler(Filters.text & ~Filters.command, question3)],
            4: [MessageHandler(Filters.text & ~Filters.command, view)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
)

def run(TOKEN):
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()
