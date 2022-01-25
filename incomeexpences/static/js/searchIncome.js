const tableOutput  =  document.querySelector('.table-output');
const searchField =  document.querySelector("#searchField");
const  appTable =  document.querySelector('.app-table');
const  paginationContainer  =  document.querySelector('.pagination-container');
const tableBody = document.querySelector('.table-body');
tableOutput.style.display = "none";

searchField.addEventListener("keyup" ,  (e)=>{
    const  searchValue =  e.target.value
    if(searchValue.trim().length > 0){
    paginationContainer.style.display = "none";
    tableBody.innerHTML = "";
        fetch('search_incomes'  ,  {
            body:JSON.stringify ({'searchIncomeText' :  searchValue }) ,
            method: 'POST',
        }).then(res => res.json())
        .then(data =>{
            console.log("data" , data)

            appTable.style.display = "none";
            if(data.length===0){
                tableOutput.innerHTML =  "No results match" ;
                paginationContainer.style.display = "none"
            }
            else{
            tableOutput.style.display = "block";
            appTable.style.display = "none";
            data.forEach((item)=>{
            tableBody.innerHTML +=
                `<tr>
                        <td>${item.amount}</td>
                        <td>${item.source}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        <td>
                        <a href="{% url 'edit-incomes' item.id  %}"
                            class  ="btn btn-outline-success btn-sm text-center"
                           style="border-radius :  9px ;  opacity :  0.9">Edit</a>
                    </td>
                <tr> `;
            })
            }
        })
    }
    else{
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});