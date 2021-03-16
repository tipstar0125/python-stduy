"use strict";

let items = [];
let orders = [];
const master_tbody = document.getElementById('mater-tbody');
const order_tbody = document.getElementById('order-tbody');
const input_id_select = document.getElementById('input_id_select');

class Item {
    constructor(id, name, price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }

    view() {

        const tr = document.createElement('tr');
        const td_id = document.createElement('td');
        const td_name = document.createElement('td');
        const td_price = document.createElement('td');
        const selected_option = document.createElement('option');

        td_id.textContent = this.id;
        td_name.textContent = this.name;
        td_price.textContent = this.price;
        selected_option.textContent = this.id

        tr.appendChild(td_id);
        tr.appendChild(td_name);
        tr.appendChild(td_price);
        master_tbody.appendChild(tr);
        input_id_select.appendChild(selected_option);
    }
}

class Order {
    constructor(id, name, price, number) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.number = number;
        this.subtotal = price * number;
    }

    view() {

        const tr = document.createElement('tr');
        const td_id = document.createElement('td');
        const td_name = document.createElement('td');
        const td_number = document.createElement('td');
        const td_subtotal = document.createElement('td');

        td_id.textContent = this.id;
        td_name.textContent = this.name;
        td_number.textContent = this.number;
        td_subtotal.textContent = this.subtotal;

        tr.appendChild(td_id);
        tr.appendChild(td_name);
        tr.appendChild(td_number);
        tr.appendChild(td_subtotal);
        order_tbody.appendChild(tr);

    }
}

const clearMasterView = () => {

    const trNodes = document.querySelectorAll('#mater-tbody>tr');
    const optionNodes = document.querySelectorAll('#input_id_select>option');

    if (trNodes) {
        trNodes.forEach(trNode => {
            master_tbody.removeChild(trNode);
        });
    }

    if (optionNodes) {
        optionNodes.forEach(optionNode => {
            input_id_select.removeChild(optionNode);
        });

        const selected_option = document.createElement('option');
        selected_option.textContent = 'Please select'
        input_id_select.appendChild(selected_option);
    }
};

const clearOrderView = () => {

    const trNodes = document.querySelectorAll('#order-tbody>tr');

    if (trNodes) {
        trNodes.forEach(trNode => {
            order_tbody.removeChild(trNode);
        });
    }
};

// 登録ボタンがクリックされた時の処理
master_submit.addEventListener('click', () => {

    const file_name = source.value;

    if (!file_name) {
        window.alert('商品マスタを入力してください');
    } else {
        eel.item_master_register(file_name);
    }
})

// IDが変更された時の処理
input_id_select.addEventListener('change', () => {

    const selected_item_name = document.getElementById('selected_item_name');
    const item = items.find(item => item.id === input_id_select.value);
    selected_item_name.textContent = item.name;
})

// 購入ボタンがクリックされた時の処理
buy_submit.addEventListener('click', () => {
    const order_code = document.getElementById('input_id_select').value;
    const order_number = document.getElementById('order_number').value;
    if (!order_code || !order_number) {
        window.alert('商品コード、個数を入力してください');
    } else {
        eel.buy_register(order_code, order_number);
    }
})

// 取消ボタンがクリックされた時の処理
buy_cancel.addEventListener('click', () => {

        eel.buy_cancel();

})

// クリアボタンがクリックされた時の処理
buy_clear.addEventListener('click', () => {

        eel.buy_clear();

})

// 精算ボタンがクリックされた時の処理
payoff_submit.addEventListener('click', () => {
    const receive_money = document.getElementById('receive_money').value;
    if (!receive_money) {
        window.alert('お預かり金額を入力してください');
    } else {
        eel.payoff(receive_money);
    }
})


eel.expose(view_error)
function view_error(text){
    window.alert(text);
}

eel.expose(register_completed)
function register_completed(item_master) { 
    
    const html = '<div class="alert alert-success mb-0 d-flex justify-content-center" role="alert">登録完了</div>';
    $("#register-completed").children().remove();
    $("#register-completed").append(html);

    const keys = Object.keys(item_master);
    const indexes = Object.keys(item_master[keys[0]]);
    items = [];

    indexes.forEach(index => {
        const id = item_master.item_code[index];
        const item = item_master.item_name[index];
        const price = item_master.price[index];
        items.push(new Item(id, item, price));
    });

    clearMasterView();

    items.forEach(item => {
        item.view();
    });

}

eel.expose(view_total_cost)
function view_total_cost(total_cost, order_list){

    document.getElementById('total_cost').textContent = '合計金額：' + total_cost + '円';

    orders = [];

    order_list.forEach(order => {

        const id = order.item_code;
        const number = order.item_num;
        const item = items.find(item => item.id === id);
        orders.push(new Order(id, item.name, item.price, number));

    });

    clearOrderView();

    orders.forEach(order => {
        order.view();
    });

}

eel.expose(view_return_money)
function view_return_money(return_money){
    document.getElementById('return_money').textContent = 'お釣り：' + return_money + '円';
}