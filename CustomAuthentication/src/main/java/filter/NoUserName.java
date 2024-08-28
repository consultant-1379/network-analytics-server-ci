package filter;

import com.spotfire.server.security.CustomAuthenticatorException;

/**
 * Created by ezbrest on 08/09/2017.
 */
public class NoUserName extends CustomAuthenticatorException {
    public NoUserName(String message) {
        super(message);
    }
}
