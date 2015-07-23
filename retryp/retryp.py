#! /usr/bin/env pytho

import logging, logtool, random, time, wrapt

LOG = logging.getLogger (__name__)
DEFAULT_RETRIES = 10
DEFAULT_DELAY = 10
DEFAULT_BACKOFF = 10
MAX_RETRIES = 1073741823

class FailedTooOften (Exception):
  pass

@wrapt.decorator
class retryp (object): # pylint: disable=C0103,R0903

  @logtool.log_call (log_exit = False)
  def __init__ (self, count = DEFAULT_RETRIES,
                delay = DEFAULT_DELAY, backoff = DEFAULT_BACKOFF, jitter = 0,
                refuse_rc_fn = None, refuse_exc_fn = None,
                expose_last_exc = False, log_faults = False,
                log_faults_level = logging.DEBUG):
    self.count = count if count else MAX_RETRIES # Nothing is forever
    self.delay = delay
    self.backoff = backoff
    self.jitter = jitter
    self.refuse_rc_fn = refuse_rc_fn
    self.refuse_exc_fn = refuse_exc_fn
    self.expose_last_exc = expose_last_exc
    self.log_faults = log_faults
    self.log_faults_level = log_faults_level

  @logtool.log_call (log_exit = False)
  def __call__ (self, fn, instance, args, kwargs):
    for attempt in xrange (self.count):
      LOG.debug ("Retry attempt #%d/%d to call %s:%s:%s", attempt, self.count,
                 fn.__class__.__name__, fn.__module__, fn.__name__)
      try:
        rc = fn (*args, **kwargs)
        if self.refuse_rc_fn and self.refuse_rc_fn (rc):
          LOG.debug ("RC refused...retrying...: %s", rc)
          continue
        return rc
      except Exception as e:
        if self.log_faults:
          logtool.log_fault (e, level = self.log_faults_level)
        else:
          LOG.info ("Attempt %d failed: %s", attempt, e)
        if self.refuse_exc_fn and self.refuse_exc_fn (e):
          LOG.debug ("Exception refused: %s", e)
          raise
        if self.expose_last_exc and attempt == self.count - 1: # Last one
          LOG.debug ("Exposing last exception: %s", e)
          raise
        zzz = (self.delay
               + ((-1 if random.random () < 0.5 else 1)
                  * (self.jitter * random.random ()))
               + attempt * self.backoff)
        LOG.debug ("Retryp delay: %d seconds", zzz)
        time.sleep (zzz)
    raise FailedTooOften
