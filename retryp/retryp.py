#! /usr/bin/env pytho

import logging, logtool, random, time, wrapt

LOG = logging.getLogger (__name__)
DEFAULT_RETRIES = 10
DEFAULT_DELAY = 10
DEFAULT_BACKOFF = 10
MAX_RETRIES = 1073741823

class FailedTooOften (Exception):
  pass

@wrapt.decorator # pylint: disable=too-few-public-methods
class retryp (object):

  @logtool.log_call (log_exit = False)
  def __init__ (self, count = DEFAULT_RETRIES,
                delay = DEFAULT_DELAY, backoff = DEFAULT_BACKOFF, jitter = 0,
                refuse_rc_fn = None, refuse_exc_fn = None,
                expose_last_exc = False, log_faults = False,
                log_faults_level = logging.DEBUG, name = None):
    self.count = count if count else MAX_RETRIES # Nothing is forever
    self.delay = delay
    self.backoff = backoff
    self.jitter = jitter
    self.refuse_rc_fn = refuse_rc_fn
    self.refuse_exc_fn = refuse_exc_fn
    self.expose_last_exc = expose_last_exc
    self.log_faults = log_faults
    self.log_faults_level = log_faults_level
    self.name = (" (%s) " % name) if name else " "

  @logtool.log_call (log_exit = False, log_args = False)
  def __call__ (self, fn, instance, args, kwargs):
    for attempt in range (self.count):
      LOG.debug ("Retry%sattempt #%d/%d to call %s:%s:%s",
                 self.name, attempt, self.count,
                 fn.__class__.__name__, fn.__module__, fn.__name__)
      wiggle = ((-1 if random.random () < 0.5 else 1)
                * (self.jitter * random.random ()))
      zzz = abs (self.delay + wiggle) + attempt * self.backoff
      try:
        rc = fn (*args, **kwargs)
        if self.refuse_rc_fn and self.refuse_rc_fn (rc):
          LOG.debug ("RC%srefused...retrying...: %s", self.name, rc)
          continue
        if attempt:
          LOG.info ("Attempt%s#%d/#%d SUCCEEDED!",
                    self.name, attempt, self.count)
        return rc
      except Exception as e:
        if self.log_faults:
          logtool.log_fault (e, level = self.log_faults_level)
        LOG.info ("Attempt%s#%d/#%d failed: %r  Delay: %d seconds",
                  self.name, attempt, self.count, e, zzz)
        if self.refuse_exc_fn and self.refuse_exc_fn (e):
          LOG.debug ("%sException refused: %s", self.name, e)
          raise
        if self.expose_last_exc and attempt == self.count - 1: # Last one
          LOG.debug ("%sExposing last exception: %r", self.name, e)
          raise
        time.sleep (zzz)
    raise FailedTooOften (self.name)
