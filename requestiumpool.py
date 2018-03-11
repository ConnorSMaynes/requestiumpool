
from requestium import Session
from datetime import datetime
from http.client import BadStatusLine
from selenium.common.exceptions import WebDriverException

class RequestiumPool():
    
    def __init__( self, requestium_args, pool_size=4 ):
        '''
        Arguments:
            pool_size - int - the number of requestium sessions you want open at any 
                                given point in time. if all are being used, you wait.
            requestium_args - dict - dictionary of args for setting up requestium
            unused_destroy_timeout - int - number of seconds to wait before an unused
                                            requestium session is destroyed. Clock
                                            resets every time the session is used.
        '''
        self.available = list()
        self.inuse = list()
        self.stopped = False
        self.pool_size = pool_size
        self.requestium_args = requestium_args

    def acquire( self, acquire_wait_timeout=15 ):
        '''
        Purpose:    Get a requestium session.
        Arguments:
            acquire_wait_timeout - int - time to wait for a requestium session to free up
        Returns:
            S - requestium.Session - requestium Session object
        '''

        S = None

        # IF SESSION AVAILABLE, TAKE IT
        if len( self.available ) > 0:
            S = self.available.pop()
            self.inuse.append( S )

        # NO SESSION AVAILABLE, CREATE ONE
        elif len( self.inuse ) < self.pool_size:
            S = Session( **self.requestium_args )
            self.inuse.append( S )

        # NO SESSIONS AVAILABLE AND NO MORE ALLOWED, WAIT FOR ONE
        else:
            StartWaitTime = datetime.now()
            while ( datetime.now() - StartWaitTime ).seconds <= acquire_wait_timeout\
                    and ( len( self.inuse ) + len( self.available ) ) > 0:
                if len( self.available ) > 0:
                    S = self.available.pop()
                    self.inuse.append( S )
                    break

        return S

    def release( self, oSession ):
        '''
        Purpose:    Release the requestium session back to the pool.
                    Clear all the cookies from requests session 
                    and selenium driver.
        Arguments:
            oSession - requestium.Session - requestium Session object to release
        Returns:
            Nothing
        '''
        if oSession != None:
            try:
                oSession.cookies.clear()                            # clear all cookies from the session
                oSession.driver.delete_all_cookies()                # clear cookies from selenium driver
                if oSession in self.inuse:
                    self.inuse.remove( oSession )
                self.available.append( oSession )
            except ( ConnectionRefusedError, BadStatusLine,
                     WebDriverException, ConnectionAbortedError ):  # a few exceptions from release overlap
                pass
        return

    def destroy( self, oSession ):
        '''
        Purpose:    Destroy requestium session.
        Arguments:
            oSession - requestium.Session - requestium Session object to destroy
        Returns:
            Nothing
        '''
        if oSession != None:
            if oSession in self.inuse:
                self.inuse.remove( oSession )
            if oSession in self.available:
                self.available.remove( oSession )
            oSession.driver.quit()
            oSession = None
        return

    def stop(self):
        '''
        Purpose:    Close and destroy all requestium sessions.
        '''
        for oSession in reversed( self.inuse ):
            self.destroy( oSession )
        for oSession in reversed( self.available ):
            self.destroy( oSession )






