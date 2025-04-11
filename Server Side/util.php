<?php
function loadPos($pdo, $profile_id) {
    $stmt = $pdo->prepare('SELECT * FROM Position WHERE profile_id = :prof ORDER BY rank');
    $stmt->execute(array( ':prof' => $profile_id ));
    $positions = $stmt->fetchAll(PDO::FETCH_ASSOC);
    return $positions;
}

function loadEdu($pdo, $profile_id) {
    $stmt = $pdo->prepare('SELECT * FROM Education JOIN Institution ON Education.institution_id = Institution.institution_id WHERE profile_id = :prof ORDER BY rank');
    $stmt->execute(array( ':prof' => $profile_id ));
    $educations = $stmt->fetchAll(PDO::FETCH_ASSOC);
    return $educations;
}