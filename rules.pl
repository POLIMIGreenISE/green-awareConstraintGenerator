:- ['facts.pl'].

:- dynamic highConsumptionService/4.
:- dynamic highConsumptionConnection/5.

save_to_file(Path) :-
    open(Path, write, Stream),
    allSuggested(Constraints),
    write_results(Constraints, Stream),
    close(Stream).

allSuggested(Constraints) :-
    findall(Constraint, distinct(suggested(Constraint)), Constraints).

suggested(affinity(d(C,FC),d(S,FS),W)) :-
    deployedTo(C,FC,N), deployedTo(S,FS,M), dif(C,S), dif(N,M),
    highConsumptionConnection(C,FC,S,FS,W).

suggested(avoid(d(C,FC),N,W)) :-
    deployedTo(C,FC,_),
    highConsumptionService(C,FC,N,W).

write_results([], _).
write_results([Constraint | Tail], Stream) :-
    format(Stream, '~q.~n', [Constraint]),
    write_results(Tail, Stream).