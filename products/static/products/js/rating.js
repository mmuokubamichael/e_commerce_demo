
const rating_message = document.getElementById('successrating')
console.log(rating_message)
const one = document.getElementById('1')
const two = document.getElementById('2')
const three = document.getElementById('3')
const four = document.getElementById('4')
const five = document.getElementById('5')
const arr = [one,two,three,four,five]


const handleselection = (selection)=>{
    switch(selection){
        case '1':{
            one.classList.add('checked')
            two.classList.remove('checked')
            three.classList.remove('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
            return
        }
        case '2':{
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.remove('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
            return
        }
        case '3':{
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.add('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
            return
        }
        case '4':{
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.add('checked')
            four.classList.add('checked')
            five.classList.remove('checked')
            return
        }
        case '5':{
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.add('checked')
            four.classList.add('checked')
            five.classList.add('checked')
            return
        }

    }
}




const rate = [...document.getElementsByClassName('orderbtn')]
const ratingbtn = [...document.getElementsByClassName('ratingbtn')]

rate.forEach(rating=> rating.addEventListener('click',()=>{
    let pk = rating.getAttribute('order')
    console.log(pk)
    sessionStorage.setItem('id',pk);
    
       
}))


ratingbtn.forEach(rating=> rating.addEventListener('click',()=>{
    one.classList.remove('checked')
    two.classList.remove('checked')
    three.classList.remove('checked')
    four.classList.remove('checked')
    five.classList.remove('checked')
    
    
    $('.modal-backdrop').show();
    let pk = rating.getAttribute('order')
    console.log(pk)
    sessionStorage.setItem('id',pk);
    
       
}))

$("#item").submit(function (e){
    e.preventDefault();
    let order_id = window.sessionStorage.getItem('id')
    console.log(order_id)
    var data = {}
    const csrf = document.getElementsByName("csrfmiddlewaretoken")
    data['csrfmiddlewaretoken'] = csrf[0].value
    data['id'] = order_id
    console.log(data)
    
    $('#OrderModal').hide();
    $('.modal-backdrop').hide();

    
    
    $.ajax({
        type: 'POST',
        url: '/order_state_json/',
        data:data,
        success:function(response){
        
        
        $("#my_purchased").load(window.location.href + " #my_purchased");
        
        setTimeout(function(){
            $('#myModal').modal('show');
        },2000);
        
        },
        error: function(response){
        alert("error getting data")
        }

    })

    })


arr.forEach(item=> item.addEventListener(('mouseup'), (event)=>{
    console.log(event.target.id)
    handleselection(event.target.id)
    $("#rating_item").submit(function (e){
        e.preventDefault();
        let order_id = window.sessionStorage.getItem('id')
        console.log(order_id)
        var data = {}
        const csrf = document.getElementsByName("csrfmiddlewaretoken")
        data['rate'] = event.target.id
        data['coment'] = $("#coment").val()
        data['csrfmiddlewaretoken'] = csrf[0].value
        data['id'] = order_id
        console.log(data)
        
        //$('#myModal').modal('hide');
        $('#myModal').hide();
        $('.modal-backdrop').hide();
        

        
       
        
        
    
        $.ajax({
            type: 'POST',
            url: '/rating/',
            data:data,
            success:function(response){
            
            
            window.sessionStorage.removeItem('id')
            
            $('#rating_item')[0].reset();
            
            alert("Thanks! your Order has been reviewed successfully")
            
            //rating_message.innerHTML = `
           // <div class="alert" style="background-color:green;" role="alert">
           //     Thanks! your Order has been reviewed successfully
            //    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            //      <span aria-hidden="true">&times;</span>
            //    </button>
             // </div>
            //`
            
            
            
            //$("#content").load(window.location.href + " #content");
            window.location.reload();
            },
            
            error: function(response){
            alert("error getting data")
            }
    
        })
    
        })
}))
    
