retryp
======

From the `Jargon File <http://www.catb.org/jargon/html/p-convention.html>`:

::

    The -P Convention

    Turning a word into a question by appending the syllable ‘P’;
    from the LISP convention of appending the letter ‘P’ to denote
    a predicate (a boolean-valued function). The question should
    expect a yes/no answer, though it needn't. (See T and NIL.)

``retryp`` is yet another retry decorator, with nothing particularly
special about it other than it being both well-featured and not
rewriting or hiding the calling signature of the wrapped method (allows
for accurate code introspection -- a Big Deal for me).

Thanks go to Graham Dumpleton and his ``wrapt`` package for that latter.

Arguments
---------

count
  Default: 10

  Number of times to retry the wapped item.  If set to "0", will retry
  1073741823 times because a) that's a lot, b) give up already, and c)
  nothing lasts forever.

delay
  Default: 10 (seconds)

  The base delay between retry attempts.

backoff
  Default: 10

  A multiplicative factor applied to the delay, used to provide
  increasing backoff as subsequent attempts continue to fail.

jitter
  Default 0

  Extra random seconds will be added to each retry delay, ranging from
  0 to the value of ``jitter``.

refuse_rc_fn
  Default: None

  If provided, the return of the wrapped item will be passed as the
  only argument to this function.  If ``refuse_rc_fn (rc)`` evaluates
  to True, then no further retries will be made.

refuse_exc_fn
  Default: None

  If provided, any exception raised by the wrapped item will be passed
  as the only argument to this function.  If ``refuse_exc_fn (e)``
  evaluates to True, then the exception will be raised again and
  retry attempts will cease.

expose_last_exc
  Default: False

  By default ``retryp`` will raise ``retryp.FailedTooOften`` if the
  wrapped item continues to fail after the requested number of
  attempts.  If ``expose_last_exc`` is set, then the exception raised
  by the wrapped item will be raised if the last attempt results in an
  exception.

log_faults
  Default: False

  Log every exception raised by the wrapped item using
  logtool.log_fault.

log_faults_level
  Default: logging.CRITICAL

  Logging level at which exceptions will be logged by
  ``logtool.log_fault()`` when ``log_faults`` is set.
