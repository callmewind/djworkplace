export function spawnNotification(body, icon, title) {
  var options = {
      body: body,
      icon: icon
  };
  var n = new Notification(title, options);
}


Notification.requestPermission().then(function(result) {
  console.log(result);
});

//import('/static/notifications.js').then((m)=>{ m.spawnNotification('hola')})