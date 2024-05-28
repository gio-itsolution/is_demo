"use strict";

let task_id = ''

BX24.init(function () {
    console.log('Инициализация завершена!', BX24.isAdmin())
    const response = BX24.placement.info();
    task_id = response.options.taskId;
    const inputElement = document.querySelector('input[name="task_id"]');
    inputElement.value = task_id;
});

function myFunction() {
   BX24.callMethod("tasks.task.get", {'taskId': task_id, 'fields': ["DEADLINE"]}, function (res){
       let deadline = dayjs(res.answer.result.task['deadline']).add(1, 'day').format('DD.MM.YYYY HH:mm');
       BX24.callMethod("tasks.task.update", {'taskId': task_id, 'fields': {"DEADLINE": deadline.toString()}});
   })
}