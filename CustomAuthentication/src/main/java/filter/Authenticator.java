package filter;

import javax.naming.Context;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;
import java.util.Hashtable;

/**
 * Created by ezbrest on 18/07/2017.
 */
public class Authenticator {

    private Authenticator(){}

    public static DirContext getContext(String username,String password, String ldapURL) throws NamingException {

        if("".equals(password)){
            throw new NamingException("Null Password Value");
        }
        DirContext myContext;
        Hashtable envVars = new Hashtable();
        envVars.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        envVars.put(Context.PROVIDER_URL, ldapURL);
        envVars.put(Context.SECURITY_AUTHENTICATION, "simple");
        envVars.put(Context.SECURITY_PRINCIPAL, username);
        envVars.put(Context.SECURITY_CREDENTIALS, password);
        myContext = new InitialDirContext(envVars);
        return myContext;
    }
}
