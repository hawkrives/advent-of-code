#lang racket

(define (solve input)
  (define floor 0)
  (for ([direction input])
    (match direction
      [#\( (set! floor (add1 floor))]
      [#\) (set! floor (sub1 floor))]))
  floor)

(define examples (list 
	(list "(())" 0)
	(list "()()" 0)
	(list "(((" 3)
	(list "(()(()(" 3)
	(list "))(((((" 3)
	(list "())" -1)
	(list "))(" -1)
	(list ")))" -3)
	(list ")())())" -3)))

(for ([e examples])
  (match e
    [(list puzzle expected)
     (print puzzle)
     (display " ")
     (print expected)
     (display " ")
     (print (solve puzzle))
     (display "\n")]))