
//
// Hatena Bookmark Entrylist Widget - ver 0.1
//

$(function() {
  // user variables
  var list_title = '漢の人気エントリー道'
  var json_url = 'http://nippondanji-bm-cache.appspot.com/show'
  var entrylist_url = 'http://b.hatena.ne.jp/entrylist?url=http://nippondanji.blogspot.com/&sort=count'
  var entry_base_url = 'http://b.hatena.ne.jp/entry/'
  var hatena_icon = 'http://b.hatena.ne.jp/images/widget/favicon.gif'
  var num_entries = 16

  // initialize the hader
  var bm_header = $('<div class="bm_title"/>')
  bm_header.css({
    'background-color': '#5279e7',
    'font-weight': 'bold',
    'text-align': 'left',
    'padding-left': '5px',
    'font-size': '90%',
    'padding': '8px'
  })
  var a = $('<a/>')
  a.attr("href", entrylist_url)
  a.css({
    'color': 'crimson',
    'padding': '7px 3px',
    'margin-right': '-5px'
  })
  bm_header.append(a)
  var img = $('<img/>')
  img.attr('src', hatena_icon)
  img.css({
    'margin-right': '5px',
    'margin-bottom': '-2px'
  })
  a.append(img)
  var title = $('<span/>')
  title.text(list_title)
  a.append(title)

  // initialize the footer
  var bm_footer = $('<div class="bm_footer"/>')
  bm_footer.css({
    'background-color': '#f3f3f3',
    'font-weight': 'bold',
    'text-align': 'center',
    'font-size': '100%',
    'padding': '10px',
  })
  a = $('<a/>')
  a.attr("href", 'http://b.hatena.ne.jp/')
  footer_msg = $('<span>Hatena::Bookmark</span>')
  footer_msg.css('color', 'lightsteelblue')
  a.append(footer_msg)
  bm_footer.append(a)

  // main logic
  $.ajax({
    dataType: "jsonp",
    type: "GET",
    data: {
        "url": "http://nippondanji.blogspot.com/",
        "max-results": num_entries,
    },
    cache: true,
    url: json_url,
    success: function (data) {
      var widget = $('#nippondanji_hatena_bookmark_widget')
      widget.css({
        'margin': '0',
        'padding': '0',
        'border': '0',
        'font-family': 'arial, helvetica, verdana, sans-serif',
        'font-size': '100%',
        'line-heigh': '1.1'
      })
      widget.append(bm_header)
      for(i = 0; i < num_entries; i++) {
        entry_link = $("<a/>")
        entry_link.attr("href", data[i].link)
        entry_link.text(data[i].title)
        entry_link.css({
          'display': 'block',
          'padding': '7px 3px',
          'height': '2.0em'
        })

        entry_box = $("<div/>")
        entry_box.attr("class", "bm_entry")
        entry_box.css({
          'background-color': '#f3f3f3',
          'font-weight': 'normal',
          'text-align': 'left',
          'padding-left': '5px',
          'font-size': '90%',
          'border-bottom': '1px solid #ddd',
          'position': 'relative',
          'display': 'block',
          'vertical-align': 'bottom',
          'height': '4.0em'
        })

        counter_box = $("<span/>")
        counter_box.attr("class", "bm_count")
        counter_box.css({
          'position': 'absolute',
          'bottom': '3px',
          'right': '5px',
          'overflow': 'hidden',
          'display': 'block'
        })

        counter_link = $("<a/>")
        counter_link.attr("href", entry_base_url + data[i].link)
        counter_link.text(data[i].count + 'users')
        counter_link.css('text-decoration', 'underline')

        var counter_deco
        if(data[i].count < 5) {
          counter_deco = $('<span>')
        } else if(data[i].count < 10) {
          counter_deco = $('<em/>')
          counter_link.css({
            'background-color': '#fff0f0',
            'font-weight': 'bold',
            'display': 'inline',
            'font-style': 'normal',
            'color': 'red',
          })

        } else {
          counter_deco = $('<strong/>')
          counter_link.css({
            'background-color': '#ffcccc',
            'font-weight': 'bold',
            'font-style': 'normal',
            'display': 'inline',
            'color': 'red'
          })
        }

        widget.append(
          entry_box.append(
            entry_link
          ).append(
            counter_box.append(
              counter_deco.append(
                counter_link
              )
            )
          )
        )
      }
      widget.append(bm_footer)
    }
  })
});

document.write(['<style type="text/css">',
  '<!--',
  '.nippondanji_hatena_bookmark_widget div a:link {',
    'color:blue;',
    'text-decoration: none;',
  '}',
  '.nippondanji_hatena_bookmark_widget div a:visited {',
    'color:purple;',
    'text-decoration: none;',
  '}',
  '.nippondanji_hatena_bookmark_widget div a:active {',
    'color:red;',
    'text-decoration: none;',
  '}',
  '.nippondanji_hatena_bookmark_widget div a:hover {',
    'text-decoration: underline;',
  '}',
  '-->',
  '</style>',
  '<div id="nippondanji_hatena_bookmark_widget" class="nippondanji_hatena_bookmark_widget" style="margin:16px; border: 1px solid #ddd;" />'].join('')
);
