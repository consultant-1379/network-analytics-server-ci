package filter;

import com.spotfire.server.security.CustomAuthenticatorException;

/**
 * Created by ezbrest on 08/09/2017.
 */
public class FailedLDAPAuthentication extends CustomAuthenticatorException{
    public FailedLDAPAuthentication(String message) {
        super(message);
    }
}
