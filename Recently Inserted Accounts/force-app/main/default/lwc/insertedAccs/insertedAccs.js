import { LightningElement, track, wire } from 'lwc';
import  getAccs from '@salesforce/apex/AccountController.getAccs';

export default class InsertedAccs extends LightningElement {
    columns = [
        {label: "Account Name", fieldName: "Name", type: "text"},
        {label: "Account Type", fieldName: "Type", type: "text"},
        {label: "Created Date", fieldName: "CreatedDate", type: "date"}
    ];
    @track accList;
    @wire (getAccs) wiredAccounts({data}) {
        this.accList = data;
    }
    count = "0 selected";
    countSelected(){
        var selectedRows = this.template.querySelector("lightning-datatable").getSelectedRows();
        this.count = selectedRows.length + " selected";
        }
}
