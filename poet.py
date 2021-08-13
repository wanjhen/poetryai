import matplotlib
import matplotlib.pyplot as plt
from IPython import display
import os
os.environ['TRIDENT_BACKEND'] = 'pytorch'
from trident import *

item='poet' 
data_provider,original_corpus=load_text(item+'.txt',unit='char',mode='next_word',is_onehot=False,sequence_length=16,return_corpus=True,sequence_start_at='random')
#全形轉半形
data_provider.traindata.data.transform_funcs=[
    ToHalfWidth()
]
t1,t2=data_provider.next()

def get_hidden_poetry(heading,temperature = 1.8):

    model =load('Models/{0}.pth'.format(item))
    # 模型千萬記得要轉換成eval模式
    model.eval()
    for  module in model.modules():
        if isinstance(module, LSTM):
            module.stateful=True
    #清除模型狀態
    for module in model.modules():
        if isinstance(module, LSTM):
            module.clear_state()
    
    model.eval()
    
    
    print()
    print('----- 以「{0}」寫歌詞'.format(heading))
    
    print('----- temperature:', temperature)
    
    result = [] #設一個result串列去接收text_generated，最後要return
    text_generated = []
    heading_idx=0
    start_string = heading[heading_idx]
    text_generated.append('[CLS]')
    text_generated.append(heading[heading_idx])
    result.append(heading) #將第一個字新增進串列
    
    heading_idx+=1
    
    
    seq = [data_provider.text2index(s) for s in start_string]
    seq.insert(0, 0)
    # seq.append(1)
    input_eval = to_tensor([seq]).long().detach()
    if ndim(input_eval)<2:
        input_eval=input_eval.expand_dims(0)
    
    
    is_finished = False
    num_generate = 0
    row_length=0
    
    sys.stdout.write(start_string)
    
    while not is_finished:
        try:
    
            predictions = model(input_eval)[-1]
            #將溫度設定僅限於機率最高的十個字
            predicted_idx=argsort(predictions)[:10]
            predicted_probs =  clip(predictions[predicted_idx],1e-8,1-1e-8)
    
            predicted_id = predicted_idx[multinomial(predicted_probs/ temperature, num_samples=1)].item()
            
            input_eval = to_tensor([[predicted_id]]).long().detach()
            
     
            if text_generated[-1]==' ' and heading_idx<len(heading):
                text_generated.append(heading[heading_idx])
                result.append(text_generated)
                #更新字頭 覆寫成為下次的輸入
                input_eval = to_tensor([[data_provider.text2index(heading[heading_idx])]]).long().detach()
                heading_idx+=1
            else:
                text_generated.append(data_provider.index2text(predicted_id))
            
            
            if ndim(input_eval) < 2:
                    input_eval = input_eval.expand_dims(0)
    
            text_generated.append(data_provider.index2text(predicted_id))
            result.append(text_generated[-1]) #將每一次生成的最後一個字新增進串列

            if len(text_generated)>15 and len(list(set(text_generated[-10:])))==1:
                is_finished = True
                break
            if text_generated[-2] == '[SEP]' and text_generated[-1] == '[PAD]':
                sys.stdout.write('\n')
                is_finished=True
                sys.stdout.flush()
            elif  text_generated[-2] == '\n' and text_generated[-1] == '\n':
                sys.stdout.write('\n')
                is_finished=True
                sys.stdout.flush()
            elif text_generated[-2] == '[SEP]' and text_generated[-1]=='[CLS]':
                sys.stdout.write('\n')
                sys.stdout.flush()
            elif text_generated[-1] not in ['[CLS]', '[SEP]', '[PAD]', '[UNK]']:
                sys.stdout.write(text_generated[-1])
                row_length += 1
                if item=='poets58'  and row_length >= 47 and text_generated[-1] in ['，', '。',' ', '[SEP]']:
                    sys.stdout.write('\n')
                    is_finished=True
                sys.stdout.flush()
            num_generate += 1
            if num_generate > 60:
                is_finished = True
    
        except Exception as e:
            print(e)
    print(' ')
    model.train()
    print()
    
    remove1 = '[CLS]'
    remove2 = '[UNK]'
    remove3 = '[PAD]'
    remove4 = '[SEP]' #把這四個標籤移除掉
    
    result = [value for value in result if value != remove1 and value != remove2 and value != remove3 and value != remove4]
    result  = '%s'*len(result) % tuple(result) #把串列連結成字串
    # result = "".join(result) #也是把串列連結成字串
    return result

#get_hidden_poetry('我')