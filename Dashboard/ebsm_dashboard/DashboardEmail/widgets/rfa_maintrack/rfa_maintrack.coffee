
class Dashing.RFAMaintrack extends Dashing.Widget
 ready: ->
    if @get('unordered')
      $(@node).find('ol').remove()
    else
      $(@node).find('ul').remove()

 onData: (data) ->
   debugger
   if data.status
     # clear existing "status-*" classes
     $(@get('node')).attr 'class', (i,c) ->
       c.replace /\bstatus-\S+/g, ''
     # add new class
     console.log data.status
     $(@get('node')).addClass "status-#{data.status}"
	
	
Dashing.Widget::accessor 'updatedAtMessage', ->
	if updatedAt = @get('updatedAt')
    timestamp = new Date(updatedAt * 1000)
    month = timestamp.getMonth() + 1
    day = timestamp.getDate()
    hours = timestamp.getHours()
    minutes = ("0" + timestamp.getMinutes()).slice(-2)
    "Last updated at #{hours}:#{minutes} on #{day}/#{month}/#{timestamp.getFullYear()}"
