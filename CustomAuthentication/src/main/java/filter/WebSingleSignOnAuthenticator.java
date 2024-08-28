package filter;

import com.spotfire.server.security.AuthenticationContext;
import com.spotfire.server.security.CustomAuthenticator;
import com.spotfire.server.security.CustomAuthenticatorException;
import com.spotfire.server.security.CustomAuthenticatorPrincipal;
import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class WebSingleSignOnAuthenticator implements CustomAuthenticator {

    private static final String[] ATTRIBUTES = { "cn", "ou" };
    private static final String CLASS = WebSingleSignOnAuthenticator.class.getName();
    private static final Logger LOGGER = Logger.getLogger(CLASS);
    private String domainControllerName ;
    private String domainControllerPassword;
    private String searchBase;
    private String ldapURL;
    private String distinguishedName;

    private String domainName;
    @Override
    public CustomAuthenticatorPrincipal authenticate(AuthenticationContext authContext)
            throws CustomAuthenticatorException {
        String headerPassword = authContext.getHeader("Password");
        String headerUserName = authContext.getHeader("UserName");

        CustomAuthenticatorPrincipal authPrincipal;
        if (headerUserName==null){
            return null;
        }
        else
        {
            if(processRequest(headerUserName,headerPassword,searchBase,domainControllerName,domainControllerPassword,ldapURL)) {
                authPrincipal= new CustomAuthenticatorPrincipal(headerUserName, domainName, headerUserName, "email");
                return authPrincipal;
            }
        }
        return null;
    }

    public void init(Map parameters) throws CustomAuthenticatorException {
        domainControllerName = (String) parameters.get("DOMAIN_CONTROLLER_NAME");
        domainControllerPassword = (String) parameters.get("DOMAIN_CONTROLLER_PASSWORD");
        searchBase = (String) parameters.get("SEARCH_BASE");
        ldapURL = (String) parameters.get("LDAP_URL");
        domainName = (String) parameters.get("DOMAIN_NAME");
    }

    public boolean processRequest(String username,String password,String searchBase, String domainControllerName,String domainControllerPassword, String ldapURL)  {

        DirContext myContext = null;
        try {
            myContext = Authenticator.getContext(domainControllerName, domainControllerPassword,ldapURL);
        } catch (Exception e) {
            LOGGER.log(Level.ALL, "Initial Domain Controller Context Failed", e);
        }
        SearchControls searchControls = new SearchControls();
        searchControls.setSearchScope(SearchControls.SUBTREE_SCOPE);
        searchControls.setReturningAttributes(ATTRIBUTES);
        String filter = "cn="+username;
        NamingEnumeration values = null;
        try {
            if(myContext!=null){
            values = myContext.search(searchBase, filter, searchControls);
            }
            else{
                return false;
            }

        } catch (NullPointerException e) {
            LOGGER.log(Level.ALL,"Base Search Failed, NullPointerException", e);
        } catch (NamingException e) {
            LOGGER.log(Level.ALL, "Base Search Failed, NamingException ", e);
        }
        if (values!=null&&values.hasMoreElements())
        {
            return performLdapSearch(password, ldapURL, values);
        }

        cleanupContext(myContext);

        return false;
    }

    private void cleanupContext(DirContext myContext) {
        if(myContext!=null){
            try {
                myContext.close();
            } catch (NamingException e) {
                LOGGER.log(Level.ALL, "myContext Naming Exception thrown", e);
            }
        }
    }

    private boolean performLdapSearch(String password, String ldapURL, NamingEnumeration values) {
        SearchResult result = null;
        try {
            result = (SearchResult) values.next();
        } catch (NamingException e) {
            LOGGER.log(Level.ALL, "Search Result Iteration Failed", e);
        }
        if(result!=null){
        distinguishedName = result.getNameInNamespace();
        }
        else{
        return false;
        }
        try{
            DirContext searchContext = Authenticator.getContext(distinguishedName, password, ldapURL);
            searchContext.close();
        }catch (Exception e) {
            LOGGER.log(Level.ALL, "searchContext.close() threw an Exception", e);
            return false;
        }
        return true;
    }
}