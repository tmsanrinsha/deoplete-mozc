# deoplete-mozc

![sonomasakada](https://user-images.githubusercontent.com/1057401/34917190-58e279aa-f986-11e7-98d0-d60c92bd71a7.gif)

Mozc（Google日本語入力）の候補をVimの補完候補として出すプラグインです。

## mozc_emacs_helperのインストール

### macOS

まず、自分がインストールしているGoogle日本語のバージョンを調べる。バージョンはIMEのアイコンから「Google 日本語入力について」をクリックして調べる事ができる。

次に、ソースコードをチェックアウトする。それぞれのバージョンのソースコードのチェックアウト方法は[mozc/release_history.md at master · google/mozc](https://github.com/google/mozc/blob/master/docs/release_history.md)に書いてある。例えば、Google日本語のバージョンが2.20だった場合は以下のコマンドでチェックアウトする。

```
git clone https://github.com/google/mozc.git -b master --single-branch
cd mozc
git checkout 280e38fe3d9db4df52f0713acf2ca65898cd697a
git submodule update --init --recursive
```

コードを以下のように修正する

```diff
$ git diff
diff --git a/src/build_mozc.py b/src/build_mozc.py
index a7a534a4..f64dadf3 100644
--- a/src/build_mozc.py
+++ b/src/build_mozc.py
@@ -167,6 +167,8 @@ def GetGypFileNames(options):
   # Include subdirectory of win32 and breakpad for Windows
   if options.target_platform == 'Windows':
     gyp_file_names.extend(glob.glob('%s/win32/*/*.gyp' % SRC_DIR))
+  elif options.target_platform == 'Mac':
+    gyp_file_names.extend(glob.glob('%s/unix/emacs/*.gyp' % SRC_DIR))
   elif options.target_platform == 'Linux':
     gyp_file_names.extend(glob.glob('%s/unix/*/*.gyp' % SRC_DIR))
     # Add ibus.gyp if ibus version is >=1.4.1.
diff --git a/src/mac/mac.gyp b/src/mac/mac.gyp
index 7a843fb0..ba56d05d 100644
--- a/src/mac/mac.gyp
+++ b/src/mac/mac.gyp
@@ -585,7 +585,6 @@
             ['branding=="GoogleJapaneseInput"', {
               'dependencies': [
                 'DevConfirmPane',
-                'codesign_client',
               ],
             }],
           ],
```

コンパイルする。mac_sdk, mac_deployment_targetは自分のmacOSのバージョンに合わせる。

```
cd mozc/src
GYP_DEFINES="mac_sdk=10.13 mac_deployment_target=10.13" python build_mozc.py gyp --noqt --branding=GoogleJapaneseInput
python build_mozc.py build -c Release unix/emacs/emacs.gyp:mozc_emacs_helper
```

コマンドを打って、以下のように表示されればOK。

```
$ echo -e '(0 CreateSession)\n(1 SendKey 1 a)' | out_mac/Release/mozc_emacs_helper
((mozc-emacs-helper . t)(version . "2.20.2673.101")(config . ((preedit-method . roman))))
((emacs-event-id . 0)(emacs-session-id . 1)(output . ()))
((emacs-event-id . 1)(emacs-session-id . 1)(output . ((id . "9104245599720096124")(mode . hiragana)(consumed . t)(preedit . ((cursor . 1)(segment ((annotation . underline)(value . "
あ")(value-length . 1)(key . "あ")))))(candidates . ((size . 2)(candidate ((index . 0)(value . "ア")(annotation . ((description . "[全] カタカナ")))(id . 0))((index . 1)(value . "あ
")(annotation . ((description . "ひらがな")))(id . 1)))(position . 0)(category . suggestion)(display-type . main)(footer . ((label . "Tabキーで選択")))(page-size . 9)))(status . ((activated . t)(mode . hiragana)(comeback-mode . hiragana)))(all-candidate-words . ((candidates ((id . 0)(index . 0)(value . "ア")(annotation . ((description . "[全] カタカナ"))))((id . 1)(index . 1)(value . "あ")(annotation . ((description . "ひらがな")))))(category . suggestion))))))
```

もしも

> 互換性のない変換エンジンプログラムに接続しています。新しい Google 日本語入力を利用するためにコンピュータを再起動してください。問題が解決されない場合は、お手数ですが一度アンインストールしてから再インストールしてください。

というメッセージがポップアップで出てきたら、コンパイルしたバージョンが違うので、コンパイルし直す。

mozc_emacs_helperは適宜PATHの通った場所に置く。

## 設定

### g:deoplete#sources#mozc#mozc_emacs_helper_path

mozc_emacs_helperのパスを設定します。環境変数PATHにあるディレクトリにおいてある場合は設定する必要はありません。

## 参考資料

- [mozc_emacs_helper を使う - N->N->N](http://d.hatena.ne.jp/hanya_orz/20170224/p1)

## 謝辞

Mozc classのコードは[yasuyuky/SublimeMozcInput](https://github.com/yasuyuky/SublimeMozcInput)のコードを参考にさせていただきました。
