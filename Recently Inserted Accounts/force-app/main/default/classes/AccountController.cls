public with sharing class AccountController {

    @AuraEnabled(cacheable=true)
    public static List<Account> getAccs() {
        List<Account> accs = [SELECT Id, Name, CreatedDate, Type FROM Account ORDER BY CreatedDate DESC LIMIT 25];
        return accs;
    }
}
