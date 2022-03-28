# 急いでいる方はこちら
**手っ取り早く概要を知りたいという方は、次の動画をご覧ください（注：音が出ます）**
https://www.youtube.com/watch?v=5tq2-lj_Rko
# densuke_guiについて
これはスケジュール調整サービス「伝助」での日時入力をより簡単にするために作成されたGUIアプリケーションです。 
また、作成されたリンクをslackに送信することも可能です。
時間の設定やメールアドレスなどは個人でお好みに編集してからお使いください。
# 使用する前に
このモジュールでは以下のライブラリを使用しているのでインストールしていないものがあれば各個人でインストールしてください。　　
>* selenium
>* pyperclip
>* chromedriver-binary
>* chromedriver-binary-auto
>* slackweb
>* PySimpleGUI　

インストールの仕方は次の通りです。
```
pip install (インストールしたいライブラリ名)
```
# 注意
* このモジュールではブラウザ操作を自動化するライブラリである「Selenium」を使用しています。しかし、伝助のサイトにはこのような自動化が良いとも悪いとも記載されていないため、使用する際はあくまで自己責任でお願いいたします。  
* ブラウザにはChromeを用いることを想定しています。Chromeがダウンロードされていない場合は正しく動作しません。
# 使い方
実行すると次のような画面が表示されるはずです。  
<img src="img/startPNG.PNG" width="500px" alt="スタート画面" title="スタート画面">  
ここでは一例として次のように入力してみます。
>* タイトルには「会議」
>* 日付を入力するは以下のように入力
> >3 1  
3 2  
3 3
>* 「時間を選択」のチェックボックスには13:00と15:00の二つにチェックを入れる  

入力後「作成」ボタンを押すとブラウザが立ち上がり、下のような伝助のページが作成されます。
<img src="img/densuke_example.PNG" width="400px" alt="作成された伝助のページ" title="作成された伝助のページ">  
本来であれば
>3/1(火) 13:00-  
3/1(火) 15:00-  
3/2(水) 13:00-  
3/2(水) 15:00-  
3/3(木) 13:00-  
3/3(木) 15:00-

と入力しなければつくれないページがあっという間に作成されました。

# 便利な機能
「次の木曜と土曜」ボタンを押すと日付の入力欄が更新され、次の木曜日と土曜日の日にちが入力されます。（「なんで木曜と土曜なの？」と思われる方もいらっしゃるかもしれませんが、これは私がよくこのツールを木曜日と土曜日の場合に使うことが多かったからです....）  
同様に「月曜から土曜」ボタンを押すと日付の入力欄が更新され次の月曜日から土曜日までの日にちが改行区切りで与えられます。

また、スクリプトの
```python:
WEB_HOOK_URL =""
```
のところにこのツールを用いて作成したリンクを送信したいslackのWebhook URLを入力していただくと、「slackのDMにリンクを送信しますか？」という項目に「はい」と答えた場合に限って指定されたslackのチャンネルにリンクが送信されます。  
(チャンネルのWebhook URLを指定すればいいのでそれがDMである必要はないのですが、私がこのツールを使うときは自分のDM宛てに送信することを想定して作ったのでこのような表記になっています。)  
~~もしメールアドレス欄に何も入力せず、かつこのslack送信機能も使わないのであればせっかく作成した伝助のページへのリンクを取得する術がなくなってしまうので十分注意してください。（つまりどちらかには値を入力して使ってください。）~~  
**(2022/03/14 追記)  
伝助のページを作成後、リンクをコピーするためのポップアップを表示する機能を追加しました。    
これによりメールアドレスやWebhook URLを設定しなくても、作成されたページのリンクを取得できるようになりました。**
# 使用例
**(2022/03/17 更新)  
GIFを見やすいものに変更しました。** この例で作成したページは[こちら](https://www.densuke.biz/list?cd=9UVskuht76SbTxrp)
<br>
![伝助作成ツール　使用例（ゆっくり）](https://user-images.githubusercontent.com/98263011/158779416-b68b4a61-d452-4851-bccd-186242f16a49.gif)  

